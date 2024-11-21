from nlds_client import nlds_client
import pytest
from nlds_client.clientlib import transactions as nlds_client
from tests.conftest import get_readable_path, get_unreadable_path, wait_completed

from .test_put import put_filelist


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
class TestPutList:
    def test_putlist_1(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS"""
        # create 2 readable files
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_1"
        )
        assert state == "COMPLETE"

    def test_putlist_1a(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Variation on test_putlist_1 but both files are the same"""
        # create 2 readable files
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_1a"
        )
        assert state == "COMPLETE"

    def test_putlist_2(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, one readable, one unreadable"""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 1)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_unreadable_path(1)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_2"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_3(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, one readable, one that doesn't exist"""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = "fake_file"
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_3"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_4(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, one unreadable, one that is readable"""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 1)
        filepath_1 = get_unreadable_path(1)
        filepath_2 = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_4"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_5(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, both unreadable"""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(0, 2)
        filepath_1 = get_unreadable_path(1)
        filepath_2 = get_unreadable_path(2)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_5"
        )
        assert state == "FAILED"

    def test_putlist_5a(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Variation on test_putlist_5 but both unreadable files are the same"""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(0, 2)
        filepath_1 = get_unreadable_path(1)
        filepath_2 = get_unreadable_path(1)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_5a"
        )
        assert state == "FAILED"

    def test_putlist_6(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, one unreadable, one doesn't exist"""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(0, 1)
        filepath_1 = get_unreadable_path(1)
        filepath_2 = "fake_file"
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_6"
        )
        assert state == "FAILED"

    def test_putlist_7(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, one doesn't exist, one readable.
        This is the same as test 3, but with the files in the opposite order.
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 1)
        filepath_1 = get_unreadable_path(1)
        filepath_2 = get_readable_path(1)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_7"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_8(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, one unreadable, one doesn't exist.
        This is the same as test 6, but with the files in the opposite order."""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(0, 1)
        filepath_1 = "fake_file"
        filepath_2 = get_unreadable_path(1)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_8"
        )
        assert state == "FAILED"

    def test_putlist_9(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test putting two files to NLDS, both don't exist."""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(0, 0)
        filepath_1 = "fake_file"
        filepath_2 = "fake_fake_file"
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_9"
        )
        assert state == "FAILED"

    def test_putlist_10(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists."""
        # create 3 readable files
        data = data_fixture_put(3, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        filepath_3 = get_readable_path(3)
        state, _ = put_filelist(data, [filepath_1], label="holding")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], label="holding", job_label="test_putlist_10"
        )
        assert state == "COMPLETE"

    def test_putlist_11(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file is unreadable, second file is readable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 1)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_unreadable_path(2)
        filepath_3 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], label="holding", job_label="test_putlist_11a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data,
            [filepath_2, filepath_3],
            label="holding",
            job_label="test_putlist_11b",
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_12(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file does not exist, second file is readable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = "fake_file"
        filepath_3 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], label="holding", job_label="test_putlist_12a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data,
            [filepath_2, filepath_3],
            label="holding",
            job_label="test_putlist_12b",
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_13(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second file is readable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = filepath_1
        filepath_3 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1], label="holding", job_label="test_putlist_13a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data,
            [filepath_2, filepath_3],
            label="holding",
            job_label="test_putlist_13b",
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_14(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second file is unreadable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 1)
        filepath_1 = get_readable_path(1)
        filepath_2 = filepath_1
        filepath_3 = get_unreadable_path(3)
        state, _ = put_filelist(
            data, [filepath_1], label="holding", job_label="test_putlist_14"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data,
            [filepath_2, filepath_3],
            label="holding",
            job_label="test_putlist_14b",
        )
        assert state == "FAILED"

    def test_putlist_15(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second file does not exist
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = filepath_1
        filepath_3 = "fake_file"
        state, _ = put_filelist(
            data, [filepath_1], label="holding", job_label="test_putlist_15a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data,
            [filepath_2, filepath_3],
            label="holding",
            job_label="test_putlist_15b",
        )
        assert state == "FAILED"

    def test_putlist_16(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second also duplicate
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], label="holding", job_label="test_putlist_16"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], label="holding", job_label="test_putlist_16"
        )
        assert state == "FAILED"

    # tests 17->23 are duplicates of 10->16 but with the label="holding"
    # substituted for a known holding id
    def test_putlist_17(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists."""
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(3, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        filepath_3 = get_readable_path(3)
        state, _ = put_filelist(data, [filepath_1], job_label="test_putlist_17a")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], holding_id=1, job_label="test_putlist_17b"
        )
        assert state == "COMPLETE"

    def test_putlist_18(self, data_fixture_put):
        """Test put two files to the NLDS, to a holding that already exists.
        First file is unreadable, second file is readable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 1)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_unreadable_path(2)
        filepath_3 = get_readable_path(2)
        state, _ = put_filelist(data, [filepath_1], job_label="test_putlist_18a")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], holding_id=1, job_label="test_putlist_18b"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_19(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file does not exist, second file is readable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = "fake_file"
        filepath_3 = get_readable_path(2)
        state, _ = put_filelist(data, [filepath_1], job_label="test_putlist_19a")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], holding_id=1, job_label="test_putlist_19b"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_20(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second file is readable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = filepath_1
        filepath_3 = get_readable_path(2)
        state, _ = put_filelist(data, [filepath_1], job_label="test_putlist_20a")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], holding_id=1, job_label="test_putlist_20b"
        )
        assert state == "COMPLETE_WITH_ERRORS"

    def test_putlist_21(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second file is unreadable
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 1)
        filepath_1 = get_readable_path(1)
        filepath_2 = filepath_1
        filepath_3 = get_unreadable_path(3)
        state, _ = put_filelist(data, [filepath_1], job_label="test_putlist_21a")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], holding_id=1, job_label="test_putlist_21b"
        )
        assert state == "FAILED"

    def test_putlist_22(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second file does not exist
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(1, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = filepath_1
        filepath_3 = "fake_file"
        state, _ = put_filelist(data, [filepath_1], job_label="test_putlist_22a")
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_2, filepath_3], holding_id=1, job_label="test_putlist_22b"
        )
        assert state == "FAILED"

    def test_putlist_23(
        self, data_fixture_put, catalog_fixture_put, monitor_fixture_put
    ):
        """Test put two files to the NLDS, to a holding that already exists.
        First file already exists (duplicate), second also duplicate
        """
        # create 1 readable and 1 unreadable file
        data = data_fixture_put(2, 0)
        filepath_1 = get_readable_path(1)
        filepath_2 = get_readable_path(2)
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], job_label="test_putlist_23a"
        )
        assert state == "COMPLETE"
        state, _ = put_filelist(
            data, [filepath_1, filepath_2], holding_id=1, job_label="test_putlist_23b"
        )
        assert state == "FAILED"
