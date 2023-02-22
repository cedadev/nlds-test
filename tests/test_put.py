from nlds_client import nlds_client
import time
import pytest

@pytest.mark.usefixtures("data_fixture", "catalog_fixture", "monitor_fixture", 
    "index_fixture", "worker_fixture", "server_fixture", "put_transfer_fixture",
    "get_transfer_fixture", "logger_fixture")
class TestPut:

    def test_put(self, data_fixture, catalog_fixture, monitor_fixture, 
                 index_fixture, worker_fixture, server_fixture, 
                 put_transfer_fixture, get_transfer_fixture, logger_fixture):
        data = data_fixture(5, 5)
        time.sleep(30)
        print("TEST TEST TEST")