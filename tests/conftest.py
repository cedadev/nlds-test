import os
import pytest
import subprocess
import os
import pathlib

from nlds_processors.catalog.catalog_worker import CatalogConsumer
from nlds_processors.monitor.monitor_worker import MonitorConsumer

class test_data:
    def __init__(self, nr=0, ur=0):
        self.nr = nr
        self.ur = ur

    def del_data(self):
        top_path = pathlib.Path(__file__).parent.parent.resolve().as_posix()
        # delete the readable files (user can read)
        for i in range(1, self.nr+1):
            path = pathlib.Path(top_path).joinpath(f"data/readable_file_{i}.txt")
            path.unlink()
        # delete the unreadable files (user does not have permission to read)
        for i in range(1, self.ur+1):
            path = pathlib.Path(top_path).joinpath(f"data/unreadable_file_{i}.txt")
            # change the file permissions first
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
            path = top_path.joinpath(f"data/readable_file_{i}.txt")
            with path.open("w") as fh:
                fh.write("!")
                # write 128K of random into the file
        # create the unreadable files (user does not have permission to read)
        for i in range(1, self.ur+1):
            path = top_path.joinpath(f"data/unreadable_file_{i}.txt")
            with path.open("w") as fh:
                fh.write("!")
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


@pytest.fixture()
def catalog_fixture():
    # run the catalog executable
    # this requires NLDS to be pip install and the `catalog_q` command to be
    # available
    consumer = CatalogConsumer()
    # delete SQLLite database if it exists to start with clean db
    db_engine = consumer.load_config_value(consumer._DB_ENGINE)
    db_options = consumer.load_config_value(consumer._DB_OPTIONS)
    db_name = "." + db_options['db_name']
    if (db_engine == "sqlite") and (os.path.exists(db_name)):
        os.unlink(db_name)
    
    p = subprocess.Popen(["catalog_q"])
    yield
    p.terminate()


@pytest.fixture()
def monitor_fixture():
    # run the monitor executable
    # this requires NLDS to be pip install and the `monitor_q` command to be
    # available
    consumer = MonitorConsumer()
    # delete SQLLite database if it exists to start with clean db
    db_engine = consumer.load_config_value(consumer._DB_ENGINE)
    db_options = consumer.load_config_value(consumer._DB_OPTIONS)
    db_name = "." + db_options['db_name']
    if (db_engine == "sqlite") and (os.path.exists(db_name)):
        os.unlink(db_name)
    
    p = subprocess.Popen(["monitor_q"])
    yield
    p.terminate()


@pytest.fixture()
def index_fixture():
    # run the indexer executable
    # this requires NLDS to be pip install and the `index_q` command to be
    # available in the path
    p = subprocess.Popen(["index_q"])
    yield
    p.terminate()


@pytest.fixture()
def worker_fixture():
    # run the worker executable
    # this requires NLDS to be pip install and the `nlds_q` command to be
    # available in the path
    p = subprocess.Popen(["nlds_q"])
    yield
    p.terminate()


@pytest.fixture()
def server_fixture():
    # run the HTTP rest server executable
    # this requires uvicorn to be installed and the `uvicorn` command to be
    # available on the path
    p = subprocess.Popen([
        "uvicorn", "nlds.main:nlds", "--reload","--log-level=trace", "--port=8000"
    ])
    yield
    p.terminate()


@pytest.fixture()
def put_transfer_fixture():
    # run the put_transfer executable
    # this requires NLDS to be pip install and the `put_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_put_q"])
    yield
    p.terminate()

@pytest.fixture()
def get_transfer_fixture():
    # run the get_transfer executable
    # this requires NLDS to be pip install and the `get_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_get_q"])
    yield
    p.terminate()


@pytest.fixture()
def logger_fixture():
    # run the logging executable
    # this requires NLDS to be pip install and the `logging_q` command to 
    # be available in the path
    p = subprocess.Popen(["logging_q"])
    yield
    p.terminate()
