from nlds_client import nlds_client
import time
import pytest
from nlds_client.clientlib import transactions as nlds_client
from nlds_client.clientlib import exceptions as nlds_error
from tests.conftest import (
    get_readable_path,
    get_unreadable_path,
    wait_completed,
    count_files,
    tag_in_holding,
)


def put_filelist(data, filepath, **kwargs):
    """Put a filelist and record the bucket it went into so we can delete it
    at the end"""
    response = nlds_client.put_filelist(filepath, **kwargs)
    state = wait_completed(response=response)
    transaction_id = response["transaction_id"]
    bucket_name = f"nlds.{transaction_id}"
    data.buckets.append(bucket_name)

    return state, response


@pytest.mark.usefixtures(
    "data_fixture_put",
    "catalog_fixture_put",
    "monitor_fixture_put",
    "index_fixture",
    "worker_fixture",
    "server_fixture",
    "put_transfer_fixture",
    "get_transfer_fixture",
    "logger_fixture",
    "pause_fixture",
)
class TestPut:

    def test_put_1(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS, without any metadata"""
        # create 1 readable file
        data = data_fixture_put(1, 0)
        filepath = get_readable_path(1)
        state, _ = put_filelist(data, [filepath], job_label="test_put_1")
        assert state == "COMPLETE"

    def test_put_2(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting an unreadable file to NLDS, without any metadata"""
        data = data_fixture_put(0, 1)
        filepath = get_unreadable_path(1)
        state, _ = put_filelist(data, [filepath], job_label="test_put_2")
        assert state == "FAILED"

    def test_put_3(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a non existing file to NLDS, without any metadata"""
        data = data_fixture_put(0, 1)
        filepath = "blah"
        state, _ = put_filelist(data, [filepath], job_label="test_put_3")
        assert state == "FAILED"

    def test_put_4(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS, with a label that doesn't
        exist"""
        data = data_fixture_put(1, 0)
        filepath = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath], label="label_1", job_label="test_put_4"
        )
        assert state == "COMPLETE"

    def test_put_5(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS, with a label that already
        exists"""
        # need to add 1 file now and 1 later
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], label="label_1", job_label="test_put_5a"
        )
        assert state == "COMPLETE"
        state, response = put_filelist(
            data, [filepath_2], label="label_1", job_label="test_put_5b"
        )
        assert state == "COMPLETE"
        # get the files in holding_id=1 - there should be two
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert n_files == 2

    def test_put_6(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS, where the file already exists
        in a holding with a label that already exists"""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath_1], label="label_1", job_label="test_put_6a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_1], label="label_1", job_label="test_put_6b"
        )
        assert state == "FAILED"

    def test_put_7(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a job_label that doesn't
        exist"""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath_1], job_label="test_put_7"
        )
        assert state == "COMPLETE"

    def test_put_8(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a job_label that does
        exist"""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], job_label="test_put_8"
        )
        assert state == "COMPLETE"
        state, response = put_filelist(
            data, [filepath_2], job_label="test_put_8"
        )
        assert state == "COMPLETE"
        # get the files in holding_id=1 - there should be one
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert n_files == 1

    def test_put_9(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that does
        not exist"""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath_1], holding_id=1, job_label="test_put_9"
        )
        assert state == "FAILED"

    def test_put_9a(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Variation on test_put_9.  Test putting a readable file to NLDS with
        a holding_id that is not legal - as it is a string."""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        # this should throw an RequestError exception as the HTTP_API is
        # expecting an integer holding_id
        with pytest.raises(nlds_error.RequestError) as re:
            _, _ = put_filelist(
                data, [filepath_1], holding_id="abcdefg", job_label="test_put_9a"
            )

    def test_put_10(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that already
        exists"""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(data, [filepath_1], job_label="test_put_10a")
        assert state == "COMPLETE"
        # holding id will be 1 as we start with a new database each time
        state, response = put_filelist(
            data, [filepath_2], holding_id=1, job_label="test_put_10b"
        )
        assert state == "COMPLETE"
        # get the files in holding_id=1 - there should be two
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert n_files == 2

    def test_put_11(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that already
        exists, where the file already exists in the holding"""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        state, _ = put_filelist(data, [filepath_1], job_label="test_put_11a")
        assert state == "COMPLETE"
        # holding id will be 1 as we start with a new database each time
        state, _ = put_filelist(
            data, [filepath_1], holding_id=1, job_label="test_put_11b"
        )
        assert state == "FAILED"

    def test_put_12(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that does not
        exist and the label does not exist"""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        state, _ = put_filelist(data, [filepath_1], job_label="test_put_12a")
        assert state == "COMPLETE"
        # holding id will be 1 as we start with a new database each time
        state, _ = put_filelist(
            data,
            [filepath_1],
            holding_id=1,
            label="holding_1",
            job_label="test_put_12b",
        )
        assert state == "FAILED"

    def test_put_13(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that does
        exist and the label does not exist - the holding id and label must match"""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], job_label="test_put_13a"
        )  # this creates the holding
        assert state == "COMPLETE"
        # holding id will be 1 as we start with a new database each time
        state, _ = put_filelist(
            data,
            [filepath_2],
            holding_id=1,
            label="holding_1",
            job_label="test_put_13b",
        )
        assert state == "FAILED"

    def test_put_14(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that does
        not exist and the label does exist - the holding id and label must match"""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], label="holding_1", job_label="test_put_14a"
        )
        assert state == "COMPLETE"
        # existing holding id will be 1 as we start with a new database each time
        # so use holding_id=2 to not exist
        state, _ = put_filelist(
            data,
            [filepath_2],
            holding_id=2,
            label="holding_1",
            job_label="test_put_14b",
        )
        assert state == "FAILED"

    def test_put_15(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to NLDS with a holding_id that exists
        in one holding and the label exists in another holding.  This will fail
        as the holding id must match the label of the holding the file is being
        added to."""
        data = data_fixture_put(3, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        filepath_3 = get_readable_path(3)
        state, _ = put_filelist(
            data, [filepath_1], label="holding_1", job_label="test_put_15a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2], label="holding_2", job_label="test_put_15b"
        )
        assert state == "COMPLETE"
        # existing holding id will be 1 as we start with a new database each
        # time, this holding will have label holding_1, so use holding_2 for the
        # test (which will have holding id=2)
        state, response = put_filelist(
            data,
            [filepath_3],
            holding_id=1,
            label="holding_2",
            job_label="test_put_15c",
        )
        assert state == "FAILED"
        # get the files in holding_id=1 - there should be only one
        user = response["user"]
        group = response["group"]
        response = nlds_client.find_file(user, group, holding_id=1)
        n_files = count_files(response)
        assert n_files == 1

    def test_put_16(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to the NLDS with a tag that does not
        exist in another holding."""
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        tag = {"author": "Neil Massey"}
        state, response = put_filelist(
            data, [filepath_1], tag=tag, job_label="test_put_16"
        )
        assert state == "COMPLETE"
        # get the tag from the holding to check it exists
        user = response["user"]
        group = response["group"]
        response = nlds_client.list_holding(user, group, tag=tag)
        # list_holding returns straight away as it is a RPC call
        tag_test = tag_in_holding(response, tag)
        assert tag_test

    def test_put_17(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to the NLDS with a tag that already
        exists in another holding."""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        tag = {"author": "Neil Massey"}
        state, _ = put_filelist(data, [filepath_1], tag=tag, job_label="test_put_17a")
        assert state == "COMPLETE"
        state, response = put_filelist(
            data, [filepath_2], tag=tag, job_label="test_put_17b"
        )
        assert state == "COMPLETE"
        # get the tag from each of the holdings to check they exist
        user = response["user"]
        group = response["group"]
        response = nlds_client.list_holding(user, group, tag=tag)
        # there should be two holdings
        n_holds = len(response["data"]["holdings"])
        assert n_holds == 2
        # list_holding returns straight away as it is a RPC call
        tag_test = tag_in_holding(response, tag)
        assert tag_test

    def test_put_18(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to a holding that already exists but
        with a new tag that doesn't already exist for the holding."""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], label="holding_1", job_label="test_put_18a"
        )
        assert state == "COMPLETE"
        tag = {"author": "Neil Massey"}
        state, response = put_filelist(
            data, [filepath_2], label="holding_1", tag=tag, job_label="test_put_18b"
        )
        assert state == "COMPLETE"
        # get the tag from each of the holdings to check they exist
        user = response["user"]
        group = response["group"]
        # list_holding returns straight away as it is a RPC call - no need
        # to wait_completed
        response = nlds_client.list_holding(user, group, tag=tag)
        # there should be one holding
        n_holds = len(response["data"]["holdings"])
        assert n_holds == 1
        tag_test = tag_in_holding(response, tag)
        assert tag_test

    def test_put_19(self, data_fixture_put, catalog_fixture_put, monitor_fixture_put):
        """Test putting a readable file to a holding that already exists and
        with a tag that already exists for the holding."""
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        tag = {"author": "Neil Massey"}
        state, _ = put_filelist(
            data, [filepath_1], label="holding_1", tag=tag, job_label="test_put_19a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2], label="holding_1", tag=tag, job_label="test_put_19b"
        )
        assert state == "COMPLETE_WITH_WARNINGS"
