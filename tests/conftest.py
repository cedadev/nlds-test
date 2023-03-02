import os
import pytest
import subprocess
import os
import pathlib
import random, string
import time

from nlds_processors.catalog.catalog_worker import CatalogConsumer
from nlds_processors.monitor.monitor_worker import MonitorConsumer
from nlds_client.clientlib import transactions as nlds_client

def get_readable_path(n):
    """Get the path of a readable file"""
    top_path = pathlib.Path(__file__).parent.parent.resolve().as_posix()
    path = pathlib.Path(top_path).joinpath(f"data/readable_file_{n}.txt")
    return path


def get_unreadable_path(n):
    """Get the path of an unreadable file"""
    top_path = pathlib.Path(__file__).parent.parent.resolve().as_posix()
    path = pathlib.Path(top_path).joinpath(f"data/unreadable_file_{n}.txt")
    return path


def wait_completed(user=None, group=None, transaction_id=None, response=None):
    """Wait until a transaction has completed using stat (get_transaction_state)
    """
    if response is not None:
        user = response['user']
        group = response['group']
        transaction_id = response['transaction_id']
    # check info supplied
    if user is None:
        raise TypeError("user parameter not supplied")
    if group is None:
        raise TypeError("group parameter not supplied")
    if transaction_id is None:
        raise TypeError("transaction_id parameter not supplied")

    finished = False
    state = "INITIALISING"
    while not finished:
        # give it some room to breathe
        time.sleep(1)
        stat_response = nlds_client.monitor_transactions(
            user=user, group=group, transaction_id=transaction_id
        )
        # stat_response is a dictionary of {details:, data:,}  
        # The transaction is [data][records][0]
        transaction = stat_response["data"]["records"][0]
        state, _ = nlds_client.get_transaction_state(transaction)

        # completion states are COMPLETE, COMPLETE_WITH_ERRORS, 
        # COMPLETE_WITH_WARNINGS, FAILED
        if (state in ["COMPLETE", "COMPLETE_WITH_ERRORS",
            "COMPLETE_WITH_WARNINGS", "FAILED"]):
            finished = True
    # return the state so we can assert against it
    return state


def count_files(response):
    n_files = 0
    for hkey in response['data']['holdings']:
        h = response['data']['holdings'][hkey]
        for tkey in h['transactions']:
            t = h['transactions'][tkey]
            for f in t['filelist']:
                n_files+=1
    return n_files

def generate_random(size):
    R = ''.join(random.choice(string.ascii_lowercase) for i in range(0, size))
    return R
    

class test_data:
    def __init__(self, nr=0, ur=0):
        self.nr = nr
        self.ur = ur

    def del_data(self):
        # delete the readable files (user can read)
        for i in range(1, self.nr+1):
            path = get_readable_path(i)
            path.unlink()
        # delete the unreadable files (user does not have permission to read)
        for i in range(1, self.ur+1):
            # change the file permissions first
            path = get_unreadable_path(i)
            path.chmod(0o777)
            path.unlink()

    def make_data(self):
        # generate the test data using Python.  The shell script is redundant.
        top_path = pathlib.Path(__file__).parent.parent.resolve()
        # check the data directory exists
        datadir = top_path.joinpath("data")
        if not datadir.exists():
            datadir.mkdir()
        # create the readable files (user can read)
        for i in range(1, self.nr+1):
            path = get_readable_path(i)
            with path.open("w") as fh:
                fh.write(generate_random(128*1024))
                # write 128K of random into the file
        # create the unreadable files (user does not have permission to read)
        for i in range(1, self.ur+1):
            path = get_unreadable_path(i)
            with path.open("w") as fh:
                fh.write(generate_random(128*1024))
                # write 128K of random into the file
            # change the file permissions
            path.chmod(0o000)


@pytest.fixture()
def data_fixture():
    # This looks complicated but actually works and gets around scoping issues
    data = test_data()
    def setup(nr, ur):
        data.nr = nr
        data.ur = ur
        data.make_data()
    yield setup
    data.del_data()


@pytest.fixture(autouse=True)
def catalog_fixture():
    # run the catalog executable
    # this requires NLDS to be pip install and the `catalog_q` command to be
    # available
    p = subprocess.Popen(["catalog_q"])
    yield
    p.terminate()

    consumer = CatalogConsumer()
    # delete SQLLite database if it exists to start next time with clean db
    db_engine = consumer.load_config_value(consumer._DB_ENGINE)
    db_options = consumer.load_config_value(consumer._DB_OPTIONS)
    db_name = "." + db_options['db_name']
    if (db_engine == "sqlite") and (os.path.exists(db_name)):
        os.unlink(db_name)



@pytest.fixture(autouse=True)
def monitor_fixture():
    # run the monitor executable
    # this requires NLDS to be pip install and the `monitor_q` command to be
    # available
    p = subprocess.Popen(["monitor_q"])
    yield
    p.terminate()

    # delete SQLLite database if it exists to start next time with clean db
    consumer = MonitorConsumer()
    db_engine = consumer.load_config_value(consumer._DB_ENGINE)
    db_options = consumer.load_config_value(consumer._DB_OPTIONS)
    db_name = "." + db_options['db_name']
    if (db_engine == "sqlite") and (os.path.exists(db_name)):
        os.unlink(db_name)


@pytest.fixture(autouse=True)
def index_fixture():
    # run the indexer executable
    # this requires NLDS to be pip install and the `index_q` command to be
    # available in the path
    p = subprocess.Popen(["index_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True)
def worker_fixture():
    # run the worker executable
    # this requires NLDS to be pip install and the `nlds_q` command to be
    # available in the path
    p = subprocess.Popen(["nlds_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True)
def server_fixture():
    # run the HTTP rest server executable
    # this requires uvicorn to be installed and the `uvicorn` command to be
    # available on the path
    p = subprocess.Popen([
        "uvicorn", "nlds.main:nlds", "--reload","--log-level=trace", "--port=8000"
    ])
    yield
    p.terminate()


@pytest.fixture(autouse=True)
def put_transfer_fixture():
    # run the put_transfer executable
    # this requires NLDS to be pip install and the `put_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_put_q"])
    yield
    p.terminate()

@pytest.fixture(autouse=True)
def get_transfer_fixture():
    # run the get_transfer executable
    # this requires NLDS to be pip install and the `get_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_get_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True)
def logger_fixture():
    # run the logging executable
    # this requires NLDS to be pip install and the `logging_q` command to 
    # be available in the path
    p = subprocess.Popen(["logging_q"])
    yield
    p.terminate()

@pytest.fixture(autouse=True)
def pause_fixture():
    time.sleep(1)