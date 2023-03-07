from nlds_client import nlds_client
import time
import pytest
from nlds_client.clientlib import transactions as nlds_client
from tests.conftest import get_readable_path, get_unreadable_path, \
                           wait_completed, count_files, tag_in_holding

@pytest.mark.usefixtures("data_fixture", "catalog_fixture", "monitor_fixture", 
    "index_fixture", "worker_fixture", "server_fixture", "put_transfer_fixture",
    "get_transfer_fixture", "logger_fixture", "pause_fixture")
class TestPut:

    def test_put_1(self, data_fixture):
        """Test putting a readable file to NLDS, without any metadata"""
        # create 1 readable file
        data = data_fixture(1, 0)
        filepath = get_readable_path(1)
        response = nlds_client.put_filelist([filepath])
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        
    def test_put_2(self, data_fixture):
        """Test putting an unreadable file to NLDS, without any metadata"""
        data = data_fixture(0, 1)
        filepath = get_unreadable_path(1)
        response = nlds_client.put_filelist([filepath])
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_3(self, data_fixture):
        """Test putting a non existing file to NLDS, without any metadata"""
        data = data_fixture(0, 1)
        filepath = "blah"
        response = nlds_client.put_filelist([filepath])
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_4(self, data_fixture):
        """Test putting a readable file to NLDS, with a label that doesn't 
        exist"""
        data = data_fixture(1, 0)
        filepath = get_readable_path(1)
        response = nlds_client.put_filelist([filepath], label="label_1")
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_put_5(self, data_fixture):
        """Test putting a readable file to NLDS, with a label that already 
        exists"""
        # need to add 1 file now and 1 later
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        response = nlds_client.put_filelist([filepath_1], label="label_1")
        response = nlds_client.put_filelist([filepath_2], label="label_1")
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the files in holding_id=1 - there should be two
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert(n_files==2)

    def test_put_6(self, data_fixture):
        """Test putting a readable file to NLDS, where the file already exists
        in a holding with a label that already exists"""
        data = data_fixture(1, 0)
        filepath_1 = get_readable_path(1)
        response = nlds_client.put_filelist([filepath_1], label="label_1")
        response = nlds_client.put_filelist([filepath_1], label="label_1")
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_7(self, data_fixture):
        """Test putting a readable file to NLDS with a job_label that doesn't 
        exist"""
        data = data_fixture(1, 0)
        filepath_1 = get_readable_path(1)
        response = nlds_client.put_filelist([filepath_1], job_label="job_1")
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_put_8(self, data_fixture):
        """Test putting a readable file to NLDS with a job_label that does 
        exist"""
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        response = nlds_client.put_filelist([filepath_1], job_label="job_1")
        response = nlds_client.put_filelist([filepath_2], job_label="job_1")
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the files in holding_id=1 - there should be one
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert(n_files==1)

    def test_put_9(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that does 
        not exist"""
        data = data_fixture(1, 0)
        filepath_1 = get_readable_path(1)
        response = nlds_client.put_filelist([filepath_1], holding_id=1)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_10(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that already 
        exists"""
        data = data_fixture(2, 0)
        time.sleep(1)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        response = nlds_client.put_filelist([filepath_1])
        # holding id will be 1 as we start with a new database each time
        response = nlds_client.put_filelist([filepath_2], holding_id=1)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the files in holding_id=1 - there should be two
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert(n_files==2)

    def test_put_11(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that already 
        exists, where the file already exists in the holding"""
        data = data_fixture(1, 0)
        filepath_1 = get_readable_path(1)
        response = nlds_client.put_filelist([filepath_1])
        time.sleep(0.5)
        # holding id will be 1 as we start with a new database each time
        response = nlds_client.put_filelist([filepath_1], holding_id=1)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_12(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that does not 
        exist and the label does not exist"""
        data = data_fixture(1, 0)
        filepath_1 = get_readable_path(1)
        response = nlds_client.put_filelist([filepath_1])
        time.sleep(0.5)
        # holding id will be 1 as we start with a new database each time
        response = nlds_client.put_filelist(
            [filepath_1], holding_id=1, label="holding_1"
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_13(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that does 
        exist and the label does not exist - the holding id should have 
        precedence"""
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        response = nlds_client.put_filelist([filepath_1]) # this creates the holding
        # holding id will be 1 as we start with a new database each time
        response = nlds_client.put_filelist(
            [filepath_2], holding_id=1, label="holding_1"
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the files in holding_id=1 - there should be two
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert(n_files==2)

    def test_put_14(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that does 
        not exist and the label does exist - the holding id should have 
        precedence and the test should fail"""
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        response = nlds_client.put_filelist([filepath_1], label="holding_1")
        # existing holding id will be 1 as we start with a new database each time
        # so use holding_id=2 to not exist
        response = nlds_client.put_filelist(
            [filepath_2], holding_id=2, label="holding_1"
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_put_15(self, data_fixture):
        """Test putting a readable file to NLDS with a holding_id that exists 
        and the label exists - the holding id should have precedence and the 
        test should complete with two holdings created, and the third file 
        added to the second holding"""
        data = data_fixture(3, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        filepath_3 = get_readable_path(3)
        response = nlds_client.put_filelist([filepath_1], label="holding_1")
        response = nlds_client.put_filelist([filepath_2], label="holding_2")
        # existing holding id will be 1 as we start with a new database each 
        # time, this holding will have label holding_1, so use holding_2 for the
        # test (which will have holding id=2)
        response = nlds_client.put_filelist(
            [filepath_3], holding_id=1, label="holding_2"
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the files in holding_id=1 - there should be two
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert(n_files==2)

    def test_put_16(self, data_fixture):
        """Test putting a readable file to the NLDS with a tag that does not
        exist in another holding."""
        data = data_fixture(1, 0)
        filepath_1 = get_readable_path(1)
        tag = {"author":"Neil Massey"}
        response = nlds_client.put_filelist([filepath_1], tag=tag)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the tag from the holding to check it exists
        user = response["user"]
        group = response["group"]
        response = nlds_client.list_holding(user, group, tag=tag)
        # list_holding returns straight away as it is a RPC call
        tag_test = tag_in_holding(response, tag)
        assert(tag_test)

    def test_put_17(self, data_fixture):
        """Test putting a readable file to the NLDS with a tag that already 
           exists in another holding."""
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        tag = {"author":"Neil Massey"}
        response = nlds_client.put_filelist([filepath_1], tag=tag)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        response = nlds_client.put_filelist([filepath_2], tag=tag)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the tag from each of the holdings to check they exist
        user = response["user"]
        group = response["group"]
        response = nlds_client.list_holding(user, group, tag=tag)
        # there should be two holdings
        n_holds = len(response['data']['holdings'])
        assert(n_holds == 2)
        # list_holding returns straight away as it is a RPC call
        tag_test = tag_in_holding(response, tag)
        assert(tag_test)

    def test_put_18(self, data_fixture):
        """Test putting a readable file to a holding that already exists but
        with a new tag that doesn't already exist for the holding."""
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        response = nlds_client.put_filelist([filepath_1], label="holding_1")
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        tag = {"author":"Neil Massey"}
        response = nlds_client.put_filelist(
            [filepath_2], label="holding_1", tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # get the tag from each of the holdings to check they exist
        user = response["user"]
        group = response["group"]
        response = nlds_client.list_holding(user, group, tag=tag)
        # there should be one holding
        n_holds = len(response['data']['holdings'])
        assert(n_holds == 1)
        # list_holding returns straight away as it is a RPC call
        tag_test = tag_in_holding(response, tag)
        assert(tag_test)

    def test_put_19(self, data_fixture):
        """Test putting a readable file to a holding that already exists and
        with a tag that already exists for the holding."""
        data = data_fixture(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        tag = {"author":"Neil Massey"}
        response = nlds_client.put_filelist(
            [filepath_1], label="holding_1", tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        response = nlds_client.put_filelist(
            [filepath_2], label="holding_1", tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_WARNINGS")