import os
import pytest
import subprocess
import os
import pathlib, shutil
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


def get_data_dir():
    # generate the test data using Python.  The shell script is redundant.
    top_path = pathlib.Path(__file__).parent.parent.resolve()
    datadir = top_path.joinpath("data").resolve()
    return datadir


def get_target_dir():
    # generate the test data using Python.  The shell script is redundant.
    top_path = pathlib.Path(__file__).parent.parent.resolve()
    targetdir = top_path.joinpath("target").resolve()
    return targetdir


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
    # there is a problem that this function may never complete if the state does
    # not reach any of the states below
    # keep a counter (in seconds) of the number of loops so we can exit
    n_loops = 0
    MAX_LOOPS = 20
    while not finished and n_loops < MAX_LOOPS:
        # give it some room to breathe
        time.sleep(1)
        n_loops+=1
        stat_response = nlds_client.monitor_transactions(
            user=user, group=group, transaction_id=transaction_id
        )
        # stat_response is a dictionary of {details:, data:,}  
        # The transaction is [data][records][0]
        data = stat_response["data"]["records"]
        if len(data) > 0:
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


def tag_in_holding(response, tag_test):
    result = False
    for h in response['data']['holdings']:
        tags = h['tags']
        t = all(tags.get(key, None) == val for key,val in tag_test.items())
        if result == False:
            result = t
        else:
            result &= t

    return result


def generate_random(size):
    R = ''.join(random.choice(string.ascii_lowercase) for i in range(0, size))
    return R
    

def delete_catalog():
    # called at the end of catalog_fixture_put and catalog_fixture_get
    consumer = CatalogConsumer()
    # delete SQLLite database if it exists to start next time with clean db
    db_engine = consumer.load_config_value(consumer._DB_ENGINE)
    db_options = consumer.load_config_value(consumer._DB_OPTIONS)
    db_name = "." + db_options['db_name']
    if (db_engine == "sqlite") and (os.path.exists(db_name)):
        os.unlink(db_name)


def delete_monitor():
    # delete SQLLite database if it exists to start next time with clean db
    consumer = MonitorConsumer()
    db_engine = consumer.load_config_value(consumer._DB_ENGINE)
    db_options = consumer.load_config_value(consumer._DB_OPTIONS)
    db_name = "." + db_options['db_name']
    if (db_engine == "sqlite") and (os.path.exists(db_name)):
        os.unlink(db_name)


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

        # remove the data directory and target directory (if they exist)
        datadir = get_data_dir()
        if datadir.exists():
            datadir.rmdir()

        target = get_target_dir()
        if target.exists():
            shutil.rmtree(target)
        

    def make_data(self):
        # check the data directoryand target  exists
        datadir = get_data_dir()
        if not datadir.exists():
            datadir.mkdir()
        target = get_target_dir()
        if not target.exists():
            target.mkdir()

        # create the readable files (user can read)
        for i in range(1, self.nr+1):
            path = get_readable_path(i)
            with path.open("w") as fh:
                # write 128K of random into the file
                fh.write(generate_random(128*1024))
        # create the unreadable files (user does not have permission to read)
        for i in range(1, self.ur+1):
            path = get_unreadable_path(i)
            with path.open("w") as fh:
                # write 128K of random into the file
                fh.write(generate_random(128*1024))
            # change the file permissions
            path.chmod(0o000)

    def upload_data(self, sr=1, er=-1, label=None, tag={}):
        # upload data to the object storage so that it is available to the
        # get tests
        # the data should already have been created by a call to data.make_data()
        filelist = []
        # build a list of the files
        if er == -1:
            er = self.nr
        for i in range(sr, er+1):
            path = get_readable_path(i)
            filelist.append(path)
        # upload the filepath
        response = nlds_client.put_filelist(filelist, label=label, tag=tag)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")


@pytest.fixture(scope="function")
def data_fixture_put():
    # This looks complicated but actually works and gets around scoping issues
    print("CREATING DATA")
    data = test_data()
    def setup(nr, ur):
        data.nr = nr
        data.ur = ur
        data.make_data()
    yield setup
    data.del_data()


@pytest.fixture(scope="function")
def catalog_fixture_put(worker_fixture):
    # run the catalog executable
    # this requires NLDS to be pip install and the `catalog_q` command to be
    # available
    print("LAUNCHING CATALOG")
    p = subprocess.Popen(["catalog_q"])
    yield
    p.terminate()
    # cleanup
    delete_catalog()


@pytest.fixture(scope="function")
def monitor_fixture_put(worker_fixture):
    # run the monitor executable
    # this requires NLDS to be pip install and the `monitor_q` command to be
    # available
    print("LAUNCHING MONITOR")
    p = subprocess.Popen(["monitor_q"])
    yield
    p.terminate()
    # cleanup
    delete_monitor()


@pytest.fixture(autouse=True, scope="class")
def index_fixture(worker_fixture):
    print("LAUNCHING INDEXER")
    # run the indexer executable
    # this requires NLDS to be pip install and the `index_q` command to be
    # available in the path
    p = subprocess.Popen(["index_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True, scope="class")
def worker_fixture(server_fixture, logger_fixture):
    print("LAUNCHING WORKER")
    # run the worker executable
    # this requires NLDS to be pip install and the `nlds_q` command to be
    # available in the path
    p = subprocess.Popen(["nlds_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True, scope="session")
def server_fixture():
    print("LAUNCHING SERVER")
    # run the HTTP rest server executable
    # this requires uvicorn to be installed and the `uvicorn` command to be
    # available on the path
    p = subprocess.Popen([
        "uvicorn", "nlds.main:nlds", "--reload","--log-level=trace", "--port=8000"
    ])
    yield
    p.terminate()


@pytest.fixture(autouse=True, scope="class")
def put_transfer_fixture(worker_fixture):
    print("LAUNCHING PUT TRANSFER")
    # run the put_transfer executable
    # this requires NLDS to be pip install and the `put_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_put_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True, scope="class")
def get_transfer_fixture(worker_fixture):
    print("LAUNCHING GET TRANSFER")
    # run the get_transfer executable
    # this requires NLDS to be pip install and the `get_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_get_q"])
    yield
    p.terminate()


@pytest.fixture(autouse=True, scope="class")
def logger_fixture():
    print("LAUNCHING LOGGER")
    # run the logging executable
    # this requires NLDS to be pip install and the `logging_q` command to 
    # be available in the path
    p = subprocess.Popen(["logging_q"])
    yield
    # give the logger time to clear up
    time.sleep(1)
    p.terminate()


@pytest.fixture(autouse=True, scope="function")
def pause_fixture():
    print("SLEEPING")
    time.sleep(1)

# These fixtures (data_fixture_get, catalog_fixture_get and monitor_fixture_get)
# look very similar to their _put counterparts.  However, they do have different
# scopes - they are created at the class level, so that the data is available
# in the NLDS catalog and Object Storage for each get test

@pytest.fixture(scope="class")
def data_fixture_get(catalog_fixture_get, monitor_fixture_get):
    # Simpler version of data_fixture_put, which just makes some test data
    # and uploads it to the NLDS
    print("CREATING DATA")
    data = test_data()
    data.nr = 15
    data.ur = 0
    data.make_data()
    data.upload_data(1, 5, label="test_holding_1")
    data.upload_data(6, 10, label="test_holding_2", tag={"filelist":"6 to 10"})
    data.upload_data(11, 15, label="test_holding_3", tag={"filelist":"11 to 15"})
    yield
    data.del_data()


@pytest.fixture(scope="class")
def catalog_fixture_get(worker_fixture):
    # run the catalog executable
    # this requires NLDS to be pip install and the `catalog_q` command to be
    # available
    print("LAUNCHING CATALOG")
    p = subprocess.Popen(["catalog_q"])
    yield
    p.terminate()
    delete_catalog()


@pytest.fixture(scope="class")
def monitor_fixture_get(worker_fixture):
    # run the monitor executable
    # this requires NLDS to be pip install and the `monitor_q` command to be
    # available
    print("LAUNCHING MONITOR")
    p = subprocess.Popen(["monitor_q"])
    yield
    p.terminate()
    delete_monitor()