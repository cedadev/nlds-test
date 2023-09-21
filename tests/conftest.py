import os
import pytest
import subprocess
import os
import pathlib, shutil
import random, string
import time, json
import minio

from nlds_processors.catalog.catalog_worker import CatalogConsumer
from nlds_processors.monitor.monitor_worker import MonitorConsumer
from nlds_client.clientlib import transactions as nlds_client

def get_top_path():
    return pathlib.Path(__file__).parent.parent.resolve()

def get_readable_path(n):
    """Get the path of a readable file."""
    path = get_top_path().joinpath(f"data/readable_file_{n}.txt").resolve()
    return path


def get_unreadable_path(n):
    """Get the path of an unreadable file."""
    path = get_top_path().joinpath(f"data/unreadable_file_{n}.txt").resolve()
    return path


def get_regex_exists():
    """Get a regular expression that exists."""
    path = get_top_path().joinpath(f"data/.*").resolve()
    return path


def get_regex_notexists():
    """Get a regular expression that exists."""
    path = get_top_path().joinpath(f"data/ark*").resolve()
    return path


def get_data_dir():
    """Get the path of the directory to generate data in."""
    datadir = get_top_path().joinpath("data").resolve()
    return datadir


def get_target_dir():
    """Get the target directory path"""
    targetdir = get_top_path().joinpath("target").resolve()
    return targetdir


def get_unwriteable_target_dir():
    """Get the path of an unreadable directory"""
    target_uw = get_top_path().joinpath("target_uw").resolve()
    return target_uw
    

def get_nonexistant_target_dir():
    """Get the path of a directory that does not exist"""
    target_fake = get_top_path().joinpath("fake_dir").resolve()
    return target_fake


def count_retrieved_files():
    target_w = pathlib.Path(str(get_target_dir()) + str(get_data_dir())).resolve()
    c = 0
    for x in target_w.iterdir():
        print("FILE:", x)
        c += 1
    return c


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
        self.buckets = []


    def get_tenancy(self):
        # get the tenancy from the server config
        path = os.path.expanduser("/etc/nlds/server_config")
        fh = open(path, 'r')
        json_config = json.load(fh)
        fh.close()
        tenancy = json_config["transfer_put_q"]["tenancy"]
        return tenancy


    def get_object_store_keys(self):
        # get the accessKey and secretKey for the object storage from the
        # NLDS config
        path = os.path.expanduser("~/.nlds-config")
        fh = open(path, 'r')
        json_config = json.load(fh)
        fh.close()
        access_key = json_config["object_storage"]["access_key"]
        secret_key = json_config["object_storage"]["secret_key"]
        return access_key, secret_key


    def del_data(self):
        # Delete the (local) data created for the test
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


    def del_buckets(self):
        # Remove the buckets that were uploaded to the object store
        tenancy = self.get_tenancy()
        accessKey, secretKey = self.get_object_store_keys()
        client = minio.Minio(
            tenancy, 
            access_key=accessKey,
            secret_key=secretKey,
            secure=False
        )
        for b in self.buckets:
            # to remove a bucket:
            # 0. check the bucket exists
            # 1. get a list of objects in the bucket
            # 2. remove the objects from the bucket
            # 3. remove the bucket
            if client.bucket_exists(b):
                del_objs = client.list_objects(b, recursive=True)
                for d in del_objs:
                    client.remove_object(b, d.object_name)

                client.remove_bucket(b)


    def make_data(self):
        # check the data directoryand target  exists
        datadir = get_data_dir()
        if not datadir.exists():
            datadir.mkdir()
            # have to allow write by groups for test_get_1a - restoring to
            # original location
            datadir.chmod(0o773)

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
        # get the bucket name and add it to the list so we can delete it at
        # the end
        transaction_id = response['transaction_id']
        bucket_name = f"nlds.{transaction_id}"
        self.buckets.append(bucket_name)
        assert(state == "COMPLETE")


@pytest.fixture(scope="function")
def make_target_dirs():
    """Make and clear targets each time a test runs"""
    target = get_target_dir()
    if not target.exists():
        target.mkdir()
        # change to be writeable by everyone
        target.chmod(0o777)


    target_uw = get_unwriteable_target_dir()
    if not target_uw.exists():
        target_uw.mkdir()
        # change so readable but not writeable by the group and all
        target_uw.chmod(0o555)

    yield

    target = get_target_dir()
    if target.exists():
        shutil.rmtree(target)

    target_uw = get_unwriteable_target_dir()
    if target_uw.exists():
        target_uw.chmod(0o777)
        shutil.rmtree(target_uw)

    target_fake = get_nonexistant_target_dir()
    if target_fake.exists():
        shutil.rmtree(target_fake)


@pytest.fixture(scope="function")
def data_fixture_put():
    # This looks complicated but actually works and gets around scoping issues
    print("CREATING DATA")
    data = test_data()
    def setup(nr, ur):
        data.nr = nr
        data.ur = ur
        data.make_data()
        return data
    yield setup
    data.del_data()
    data.del_buckets()


def terminate(p):
    # terminate process p
    p.terminate()
    # wait for termination
    while p.poll() == None:
        time.sleep(0.1)
        continue

@pytest.fixture(scope="function")
def catalog_fixture_put(worker_fixture):
    # run the catalog executable
    # this requires NLDS to be pip install and the `catalog_q` command to be
    # available
    print("LAUNCHING CATALOG")
    p = subprocess.Popen(["catalog_q"])
    yield
    terminate(p)
    # cleanup
    delete_catalog()


@pytest.fixture(scope="class")
def monitor_fixture(worker_fixture):
    # run the monitor executable
    # this requires NLDS to be pip install and the `monitor_q` command to be
    # available
    print("LAUNCHING MONITOR")
    p = subprocess.Popen(["monitor_q"])
    yield
    terminate(p)
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
    terminate(p)


@pytest.fixture(autouse=True, scope="class")
def worker_fixture(server_fixture, logger_fixture):
    print("LAUNCHING WORKER")
    # run the worker executable
    # this requires NLDS to be pip install and the `nlds_q` command to be
    # available in the path
    p = subprocess.Popen(["nlds_q"])
    yield
    terminate(p)


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
    terminate(p)


@pytest.fixture(autouse=True, scope="class")
def put_transfer_fixture(worker_fixture):
    print("LAUNCHING PUT TRANSFER")
    # run the put_transfer executable
    # this requires NLDS to be pip install and the `put_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_put_q"])
    yield
    terminate(p)


@pytest.fixture(autouse=True, scope="class")
def get_transfer_fixture(worker_fixture):
    print("LAUNCHING GET TRANSFER")
    # run the get_transfer executable
    # this requires NLDS to be pip install and the `get_transfer_q` command to 
    # be available in the path
    p = subprocess.Popen(["transfer_get_q"])
    yield
    terminate(p)


@pytest.fixture(autouse=True, scope="class")
def logger_fixture():
    print("LAUNCHING LOGGER")
    # run the logging executable
    # this requires NLDS to be pip install and the `logging_q` command to 
    # be available in the path
    p = subprocess.Popen(["logging_q"])
    yield
    terminate(p)


@pytest.fixture(autouse=True, scope="function")
def pause_fixture():
    print("SLEEPING")
    # increased sleeping time due to catalog_q and monitor_q not always 
    # completing
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
    data.upload_data(6, 10, label="test_holding_2", tag={"filelist":"6 to 10", "filetype":"txt"})
    data.upload_data(11, 15, label="test_holding_3", tag={"filelist":"11 to 15", "filetype":"txt"})
    yield
    data.del_data()
    data.del_buckets()


@pytest.fixture(scope="class")
def catalog_fixture_get(worker_fixture):
    # run the catalog executable
    # this requires NLDS to be pip install and the `catalog_q` command to be
    # available
    print("LAUNCHING CATALOG")
    p = subprocess.Popen(["catalog_q"])
    yield
    terminate(p)
    delete_catalog()