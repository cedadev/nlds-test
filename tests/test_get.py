from nlds_client import nlds_client
import pytest, time, getpass
from nlds_client.clientlib import transactions as nlds_client
from tests.conftest import get_readable_path, get_unreadable_path, \
                           wait_completed, get_target_dir, \
                           get_unwriteable_target_dir, \
                           get_nonexistant_target_dir

@pytest.mark.usefixtures("data_fixture_get", "catalog_fixture_get",
    "monitor_fixture", "index_fixture", "worker_fixture", "server_fixture", 
    "put_transfer_fixture", "get_transfer_fixture", "logger_fixture", 
    "pause_fixture")
class TestGet:

    def test_get_1(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in the NLDS"""
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], target=target)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_1a(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Get a file that exists in the NLDS - no target so should restore to
        the original directory.  Does this user have write permission to that
        directory - this will determine the outcome."""
        filepath = get_readable_path(1).as_posix()
        # delete to make room
        response = nlds_client.get_filelist([filepath])
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_2(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that doesn't exist in the NLDS"""
        filepath = "fake_file"
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], target=target)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_3(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in a holding"""
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], label="test_holding_1",
                                             target=target)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_4(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that doesn't exist in a holding"""
        filepath = "fake_file"
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], label="test_holding_1",
                                            target=target)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_5(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that does exist in the NLDS, but in a different holding"""
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], label="test_holding_1",
                                            target=target)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_6(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in the NLDS, and within a holding id"""
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], holding_id=1,
                                            target=target)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_7(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that doesn't exist and use a holding_id that does"""
        filepath = "fake_file"
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], holding_id=1,
                                            target=target)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_8(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in the NLDS, from a holding id that doesn't"""
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], holding_id=3,
                                            target=target)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_9(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that doesn't exist in the NLDS, from a holding id that 
        also doesn't exist."""
        filepath = "fake_file"
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist([filepath], holding_id=3,
                                            target=target)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_10(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in the NLDS, specifying a job label"""
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        job_label = "get_1"
        response = nlds_client.get_filelist([filepath], target=target, 
                                            job_label=job_label)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_11(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get two files that exists in the NLDS, specifying the same job label.
        For each file retrieval.
        """
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        job_label = "get_1"
        response_1 = nlds_client.get_filelist([filepath_1], target=target, 
                                              job_label=job_label)
        response_2 = nlds_client.get_filelist([filepath_2], target=target, 
                                              job_label=job_label)
        state = wait_completed(response=response_1)
        assert(state == "COMPLETE")
        state = wait_completed(response=response_2)
        assert(state == "COMPLETE")

    def test_get_12(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag for a file and tag that exists in the same holding.
        """
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist([filepath], target=target, tag=tag)
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_13(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag for a file that exists but with a tag that exists in 
        a different holding.
        """
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"11 to 15"}
        response = nlds_client.get_filelist([filepath], target=target, tag=tag)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_14(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag for a file that does not exist but with a tag that 
        exists in a holding.
        """
        filepath = get_unreadable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"11 to 15"}
        response = nlds_client.get_filelist([filepath], target=target, tag=tag)
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_15(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag for a file and tag that exists in the same holding,
        with the label provided.
        """
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath], label="test_holding_", target=target, tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_16(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag and label for a file that exists in a holding with 
        the label provided.  The tag does not exist for the holding with the 
        label so the request will fail as the tag and label must match.
        """
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath], label="test_holding_1", target=target, tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_17(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag and label for a file that does not exist in a holding
        with the label provided.  The tag does exist in the holding with the 
        tag, so the request will fail as the tag and label must match.
        """
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath], label="test_holding_1", target=target, tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_18(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag and holding id for a file that exists in a holding
        with the holding id provided.  The tag also exists for the holding."""
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath], holding_id=2, target=target, tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_get_19(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag and holding id for a file that exists in a holding
        with the holding id provided.  However, the tag does not exist for the 
        holding.  This fails as the tag and holding id must match."""
        filepath = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath], holding_id=1, target=target, tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_20(self, monitor_fixture, catalog_fixture_get, 
                    data_fixture_get, make_target_dirs):
        """Test get by tag and holding id for a file that exists in a holding
        with the tag provided.  However, the tag does not exist for the 
        holding with the holding id provided.  
        This fails as the tag and holding id must resolve to the same holding."""
        filepath = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath], holding_id=1, target=target, tag=tag
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_21(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in a holding, but write to an existing but
        unreadable / unwriteable directory"""
        filepath = get_readable_path(1).as_posix()
        target = get_unwriteable_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath], label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_21a(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in the NLDS, but write to an existing but
        unreadable / unwriteable directory.
        Variation on 21 but without a label / holding."""
        filepath = get_readable_path(1).as_posix()
        target = get_unwriteable_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath], target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_get_22(self, monitor_fixture, catalog_fixture_get, 
                   data_fixture_get, make_target_dirs):
        """Get a file that exists in a holding, but write to a target that
        doesn't exist - the directory will be created, if the user has write
        permission."""
        filepath = get_readable_path(1).as_posix()
        target = get_nonexistant_target_dir()
        if (target.owner == getpass.getuser()):
            expected = "COMPLETE"
        else:
            expected = "FAILED"
        response = nlds_client.get_filelist(
            [filepath], label="test_holding_1", target=target.as_posix()
        )
        state = wait_completed(response=response)
        assert(state == expected)
