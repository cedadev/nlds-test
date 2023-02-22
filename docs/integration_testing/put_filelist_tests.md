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

| *Label*    | *HoldingID* |   *File-1*     |   *File-2*     | Outcome      | Reason |
|------------|-------------|----------------|----------------|--------------|--------|
|     -      |     -       |  **readable**  |  **readable**  | **COMPLETE** | File-1 is added, File-2 is added to new holding |
|     -      |     -       |  **readable**  | **unreadable** | **COMPLETE_WITH_ERRORS**  | File-1 is added, File-2 is not |
|     -      |     -       |  **readable**  |    **not**     | **COMPLETE_WITH_ERRORS**  | File-1 is added, File-2 is not  |
|     -      |     -       | **unreadable** |  **readable**  | **COMPLETE_WITH_ERRORS**  | File-1 is not added, File-2 is added |
|     -      |     -       | **unreadable** | **unreadable** | **FAILED**   | File-1 is not added, File-2 is not added |
|     -      |     -       | **unreadable** |    **not**     | **FAILED**   | File-1 is not added, File-2 is not added |
|     -      |     -       |    **not**     |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
|     -      |     -       |    **not**     | **unreadable** | **FAILED**   | File-1 is not added, File-2 is not added |
|     -      |     -       |    **not**     |    **not**     | **FAILED**   | File-1 is not added, File-2 is not added |
| **exists** |     -       |  **readable**  |  **readable**  | **COMPLETE** | File-1 is added, File-2 is added to holding with label|
| **exists** |     -       | **unreadable** |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| **exists** |     -       |    **not**     |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| **exists** |     -       |   **exists**   |  **readable**  | **COMPLETE_WITH_ERRORS** | File-1 is not added, File-2 is added |
| **exists** |     -       |   **exists**   | **unreadable** | **FAILED**   | File-1 is not added, File-2 is not added |
| **exists** |     -       |   **exists**   |    **not**     | **FAILED**   | File-1 is not added, File-2 is not added |
| **exists** |     -       |   **exists**   |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |
|     -      | **exists**  |  **readable**  |  **readable**  | **COMPLETE** | File-1 is added, File-2 is added to holding with label|
|     -      | **exists**  |  **readable**  | **unreadable** | **COMPLETE_WITH_ERRORS** | File-1 is added, File-2 is not added |
|     -      | **exists**  |  **readable**  |    **not**     | **COMPLETE_WITH_ERRORS** | File-1 is added, File-2 is not added |
|     -      | **exists**  |  **readable**  |   **exists**   | **COMPLETE_WITH_ERRORS** | File-1 is added, File-2 is not added |
|     -      | **exists**  | **unreadable** |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |
|     -      | **exists**  |    **not**     |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |
|     -      | **exists**  |   **exists**   |   **exists**   | **FAILED**   | File-1 is not added, File-2 is not added |

[return](./integration_testing.md)