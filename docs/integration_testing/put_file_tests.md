# Put command tests

`put` is the command that enables users to put a single file into the NLDS.
The `-u, --user` and `-g, --group` command line arguments are tested by the
[OAuth tests](./oauth_tests.md).  
The other command line options and arguments are:

  * `-l, --label` : the label of a holding to add files to.
  * `-b, --job_label` : the label to give the put job so the user can track progress.
  * `-i, --holding_id` : the numeric id of a holding to add files to.
  * `-t, --tag` : the tag of a holding to add files to.
  * `-j, --json` : return the output as JSON
  * `FILEPATH` : the path of the file to put to the NLDS.

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
  * *File* : specified by the `FILEPATH` argument.  
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

| *ID*  | *Label* | *JobLabel* | *HoldingID* | *Tag* | *File* | Outcome | Reason |
|-------|---------|------------|-------------|-------|--------|---------|--------|
| put_1 |   -     |    -       |     -       |  -    | **readable** | **COMPLETE** | file is added to new holding with label derived from transaction id |
| put_2 |   -     |    -       |     -       |  -    | **unreadable** | **FAILED** | file not readable by user |
| put_3 |   -     |    -       |     -       |  -    | **not** | **FAILED** | file not found |
| put_4 | **NOT exists** | -   |     -       |  -    | **readable** | **COMPLETE** | file is added to new holding with label |
| put_5 | **exists**|   -      |     -       |  -    | **readable** | **COMPLETE** | file is added to existing holding with label |
| put_6 | **exists**|   -      |     -       |  -    | **exists** | **FAILED** | filepath already exists in holding |
| put_7 |  -       | **NOT exists** |   -     |  -    | **readable** | **COMPLETE** | file is added to new holding with label derived from transaction id |
| put_8 |  -      |   **exists**   |   -     |  -    | **readable** | **COMPLETE** | it doesn't matter that the job label already exists|
| put_9 |  -      |    -       | **NOT exists** | -   | **readable** | **FAILED** | holding with id not found |
| put_10|  -      |    -       | **exists**     | -   | **readable** | **COMPLETE** | file added to holding |
| put_11|  -      |    -       | **exists**     | -   | **exists** | **FAILED** | filepath already exists in holding |
| put_12| **NOT exists** | -   | **NOT exists** | -   | **readable** | **FAILED** | holding with id not found |
| put_13| **NOT exists** | -   | **exists**     | -   | **readable** | **FAILED** | holding id and label must match |
| put_14| **exists**     | -   | **NOT exists** | -   | **readable** | **FAILED** | holding id and label must match |
| put_15| **exists**     | -   | **exists** but not *label*    | -   | **readable** | **FAILED** | holding id and label must match |
| put_16| **NOT exists** | -   |  -       | **NOT exists** | **readable** | **COMPLETE** | file is added to new holding and tag is added |
| put_17| **NOT exists** | -   |  -       | **exists** | **readable** | **COMPLETE** | file is added to new holding and tag is added |
| put_18| **exists** | -   |  -       | **NOT exists** | **readable** | **COMPLETE** | file is added to existing holding and tag is added |
| put_19| **exists** | -   |  -       | **exists** | **readable** | **COMPLETE_WITH_WARNINGS** | file is added to existing holding, tag is not added as already exists, warning given |

 [return](./integration_testing.md)