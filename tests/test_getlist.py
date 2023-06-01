from nlds_client import nlds_client
import pytest, time
from nlds_client.clientlib import transactions as nlds_client
from tests.conftest import get_readable_path, wait_completed,\
                           get_target_dir, get_regex_exists,\
                           get_regex_notexists, count_retrieved_files

@pytest.mark.usefixtures("data_fixture_get", "catalog_fixture_get",
    "monitor_fixture_get", "index_fixture", "worker_fixture", "server_fixture", 
    "put_transfer_fixture", "get_transfer_fixture", "logger_fixture", 
    "pause_fixture", "make_target_dirs")
class TestGetList:

    def test_getlist_1(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files that exist in the NLDS"""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_getlist_1a(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Variation on test_getlist_1 but with the same file twice"""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_getlist_2(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get one file that exists in the NLDS, and one that doesn't"""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = "fake_file"
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_3(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get one file that exists in the NLDS, and one that doesn't"""
        filepath_1 = "fake_file"
        filepath_2 = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_4(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files that do not exist in the NLDS"""
        filepath_1 = "fake_file"
        filepath_2 = "fake_file2"
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_5(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files that both exist in the holding, with a label that 
        also exists."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_getlist_6(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other existings in a
        different holding.  Supply the label for just one holding.  Expected
        behaviour is that just the file in the holding with the supplied label
        is returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_7(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other existings in a
        different holding.  Supply the label for just one holding.  Expected
        behaviour is that just the file in the holding with the supplied label
        is returned."""
        filepath_1 = get_readable_path(6).as_posix()
        filepath_2 = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], label="test_holding_2", target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_8(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other existings in a
        different holding.  Supply the label for a completely different holding.  
        Expected behaviour is neither file is returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], label="test_holding_3", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_9(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in a holding.  Supply the label a 
        holding that doesn't exist.  Expected behaviour is that the request
        fails as the holding does not exist."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], label="nolabel", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_10(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files that both exist in the holding, with an id that 
        also exists."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=1, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_getlist_11(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other exists in a
        different holding.  Supply the id for just one holding.  Expected
        behaviour is that just the file in the holding with the supplied id
        is returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=1, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_12(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other exists in a
        different holding.  Supply the id for just one holding.  Expected
        behaviour is that just the file in the holding with the supplied id
        is returned."""
        filepath_1 = get_readable_path(6).as_posix()
        filepath_2 = get_readable_path(1).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=2, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_13(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other exists in a
        different holding.  Supply an id for a completely different holding.  
        Expected behaviour is that neither file is returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(6).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=3, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_14(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in a holding.  Supply the id for a 
        holding that doesn't exist.  Expected behaviour is that the request
        fails as the holding does not exist."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=101, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_15(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files that both exist in the holding, with a tag that 
        also exists for that holding."""
        filepath_1 = get_readable_path(6).as_posix()
        filepath_2 = get_readable_path(7).as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_getlist_16(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other exists in a
        different holding.  Supply the tag for just one holding.  Expected
        behaviour is that just the file in the holding with the supplied tag
        is returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(6).as_posix()
        tag = {"filelist":"6 to 10"}
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_17(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other exists in a
        different holding.  Supply a tag for just one holding.  Expected
        behaviour is that just the file in the holding with the supplied tag
        is returned."""
        filepath_1 = get_readable_path(6).as_posix()
        filepath_2 = get_readable_path(11).as_posix()
        tag = {"filelist":"6 to 10"}
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE_WITH_ERRORS")

    def test_getlist_18(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  One exists in a holding, the other exists in a
        different holding.  Supply a tag for a completely different holding.  
        Expected behaviour is that neither file is returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(6).as_posix()
        tag = {"filelist":"11 to 15"}
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_19(self, monitor_fixture_get, catalog_fixture_get, 
                       data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in a holding.  Supply a tag for a 
        holding that doesn't exist.  Expected behaviour is that the request
        fails as the holding does not exist."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        tag = {"filelist":"15 to 16"}
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_20(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in a holding.  Supply the label and id 
        for the holding.  Expected behaviour is that both files are returned"""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=1, 
            label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")

    def test_getlist_21(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in a holding.  Supply the label for the 
        holding, but a different id.  Expected behaviour is that no files are
        returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=2, 
            label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_22(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in a holding.  Supply the id for the 
        holding, but a different label.  Expected behaviour is that no files are
        returned as holding id and label must match."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=1, 
            label="test_holding_2", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_23(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get two files.  Both exists in the same holding.  Supply the id and 
        label for the holding, but a different tag.  Expected behaviour is that 
        no files are returned."""
        filepath_1 = get_readable_path(1).as_posix()
        filepath_2 = get_readable_path(2).as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_1, filepath_2], holding_id=1, 
            label="test_holding_1", 
            tag={"filelist":"6 to 10"},
            target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_24(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists.  Should return
        15 files."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # count the files
        C = count_retrieved_files()
        assert(C == 15)

    def test_getlist_25(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exist.  Should 
        return FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_26(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists, supplying a label
        for a single holding.  Should return 5 files."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # count the files
        C = count_retrieved_files()
        assert(C == 5)

    def test_getlist_27(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists but giving a label 
        that doesn't exist.  Should FAILED."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], label="test_holding_10", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_28(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exist but giving a 
        label that does exist.  Should FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], label="test_holding_1", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_29(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exist and giving a 
        label that also doesn't exist.  Should FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], label="test_holding_10", target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_30(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists and a holding id that
        also exists.  Should return 5 files."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], holding_id=1, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # count the files
        C = count_retrieved_files()
        assert(C == 5)

    def test_getlist_31(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists but from a holding id
        that does not exist.  Should return FAILED."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], holding_id=10, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_32(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exist but giving a 
        label that does exist.  Should FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], holding_id=1, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_33(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exist and giving a 
        label that also doesn't exist.  Should FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        response = nlds_client.get_filelist(
            [filepath_regex], holding_id=10, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_34(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists and for a tag that
        exists in one holding.  Should return 5 files and COMPLETE."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        tag = {"filelist":"6 to 10"}
        response = nlds_client.get_filelist(
            [filepath_regex], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # count the files
        C = count_retrieved_files()
        assert(C == 5)

    def test_getlist_35(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists and for a tag that
        exists in two holdings.  Should return 10 files and COMPLETE."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        tag = {"filetype":"txt"}
        response = nlds_client.get_filelist(
            [filepath_regex], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "COMPLETE")
        # count the files
        C = count_retrieved_files()
        assert(C == 10)

    def test_getlist_36(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that exists and for a tag that
        does not exist.  Should return FAILED."""
        filepath_regex = get_regex_exists().as_posix()
        target = get_target_dir().as_posix()
        tag = {"filetype":"netCDF"}
        response = nlds_client.get_filelist(
            [filepath_regex], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_37(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exists and for a 
        tag that does exist in two holdings.  Should return FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        tag = {"filetype":"txt"}
        response = nlds_client.get_filelist(
            [filepath_regex], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")

    def test_getlist_38(self, monitor_fixture_get, catalog_fixture_get, 
                        data_fixture_get, make_target_dirs):
        """Get files from a regular expression that does not exists and for a 
        tag that also does not exist.  Should return FAILED."""
        filepath_regex = get_regex_notexists().as_posix()
        target = get_target_dir().as_posix()
        tag = {"filetype":"netCDF"}
        response = nlds_client.get_filelist(
            [filepath_regex], tag=tag, target=target
        )
        state = wait_completed(response=response)
        assert(state == "FAILED")