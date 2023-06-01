# Putlist command tests

`putlist` is the command that enables users to put multiple files into the NLDS
by specifying them in a plain text file.
The `-u, --user` and `-g, --group` command line arguments are tested by the
[OAuth tests](./oauth_tests.md).  
The other command line options and arguments are:

  * `-l, --label` : the label of a holding to add files to.
  * `-b, --job_label` : the label to give the put job so the user can track progress.
  * `-i, --holding_id` : the numeric id of a holding to add files to.
  * `-t, --tag` : the tag of a holding to add files to.
  * `-j, --json` : return the output as JSON
  * `FILELIST` : the path of the plain text file containing the paths of the files to put to the NLDS.

## Variables

  * *Label* : specified by the `-l` or `--label` option.  
    * **Exists** indicates that there is a holding with this label (and user) already in the catalog database.
  * *JobLabel* : specified by the `-b` or `--job_label` option.  
    * **Exists** indicates there is a job with this label already in the monitoring database.
  * *HoldingID* : specified by the `-i` or `--holding_id` option.  
    * **Exists** indicates that there is a holding with this numeric ID already in the catalog database.
  * *Tag* : specified by the `-t` or `--tag` option.  
    * **Exists** indicates that there is a holding with this tag already in the catalog database.
  * *JSON* : specified by the `j` or `--json` option.
  * *File-1* : first file in the plain text file specified by the `FILELIST` argument.  
  * *File-2* : second file in the `FILELIST` plain text file.  Two files are sufficient for testing.
    * **Readable** indicates that the file exists on the filesystem and is readable by the user.
    * **Unreadable** indicates that the file exists but the user does not have permission to read it.
    * **Not** indicates that the file does not exist on the filesystem.
    * **Exists** the file is **readable** and exists in the NLDS catalog for the holding matching "label"

### Interdependent variables

  * *Label* & *HoldingID*
  * *Label* & *HoldingID* & *File* 
  * *Label* & *HoldingID* & *Tag*

### Independent variables
  
   * *JobLabel*
   * *JSON*

### Precedence of variables
  * *HoldingID* > *Label*

## Tests

Here, just the additional functionality of `putlist` over `put` is tested.
The other variables are adequately tested by [Put command tests](./put_file_tests.md)

|    *ID*   | *Label*    | *HoldingID* |   *File-1*     |   *File-2*     | Outcome      | Reason |
|-----------|------------|-------------|----------------|----------------|--------------|--------|
| putlist_1 |     -      |     -       |  **readable**  |  **readable**  | **COMPLETE** | File-1 is added, File-2 is added to new holding |
| putlist_2 |     -      |     -       |  **readable**  | **unreadable** | **COMPLETE_WITH_ERRORS**  | File-1 is added, File-2 is not |
| putlist_3 |     -      |     -       |  **readable**  |    **not**     | **COMPLETE_WITH_ERRORS**  | File-1 is added, File-2 is not  |
| putlist_4 |     -      |     -       | **unreadable** |  **readable**  | **COMPLETE_WITH_ERRORS**  | File-1 is not added, File-2 is added |
| putlist_5 |     -      |     -       | **unreadable** | **unreadable** | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_6 |     -      |     -       | **unreadable** |    **not**     | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_7 |     -      |     -       |    **not**     |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| putlist_8 |     -      |     -       |    **not**     | **unreadable** | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_9 |     -      |     -       |    **not**     |    **not**     | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_10| **exists** |     -       |  **readable**  |  **readable**  | **COMPLETE** | File-1 is added, File-2 is added to holding with label|
| putlist_11| **exists** |     -       | **unreadable** |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| putlist_12| **exists** |     -       |    **not**     |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| putlist_13| **exists** |     -       |   **exists**   |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| putlist_14| **exists** |     -       |   **exists**   | **unreadable** | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_15| **exists** |     -       |   **exists**   |    **not**     | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_16| **exists** |     -       |   **exists**   |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_17|     -      | **exists**  |  **readable**  |  **readable**  | **COMPLETE** | File-1 is added, File-2 is added to holding with label|
| putlist_18|     -      | **exists**  |  **readable**  | **unreadable** | **COMPLETE_WITH_ERRORS** | File-1 is added, File-2 is not added |
| putlist_19|     -      | **exists**  |  **readable**  |    **not**     | **COMPLETE_WITH_ERRORS** | File-1 is added, File-2 is not added |
| putlist_20|     -      | **exists**  |  **readable**  |   **exists**   | **COMPLETE_WITH_ERRORS** | File-1 is added, File-2 is not added |
| putlist_21|     -      | **exists**  | **unreadable** |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_22|     -      | **exists**  |    **not**     |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |
| putlist_23|     -      | **exists**  |   **exists**   |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |

Test for getting other user's files

[return](./integration_testing.md)