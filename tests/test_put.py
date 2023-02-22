from nlds_client import nlds_client
import time

# def test_put(catalog_fixture, monitor_fixture, data_fixture):
#     time.sleep(30)
#     print("TEST TEST TEST")

def test_put(data_fixture):
    data = data_fixture(5, 5)
    time.sleep(3)
    print("TEST TEST TEST")