# Getlist command tests

`getlist` is the command that enables users to get a multiple files from the 
NLDS by specifying them in a plain text file.
The `-u, --user` and `-g, --group` command line arguments are tested by the
[OAuth tests](./oauth_tests.md).  
The other command line options and arguments are:

  * `-l, --label` : the label of a holding to get files from.
  * `-b, --job_label` : the label to give the getlist job so the user can track 
  progress.
  * `-i, --holding_id` : the numeric id of a holding to get files from.
  * `-t, --tag` : the tag of a holding to get files frpm.
  * `-j, --json` : return the output as JSON
  * `-r, --target` : the target path for the retrieved files.  Default is to
  retrieve the files to their original path.
  * `FILELIST` : the path of the plain text file containing the (original) paths
  of the files to get from the NLDS.

## Variables

  * *Label* : specified by the `-l` or `--label` option.  
    * **Exists** indicates that there is a holding with this label (and user) in the catalog database.  
    * **Not** indicates that the label is not in the catalog.
  * *JobLabel* : specified by the `-b` or `--job_label` option.  
    * **Exists** indicates there is a job with this label already in the monitoring database.
  * *HoldingID* : specified by the `-i` or `--holding_id` option.  
    * **Exists** indicates that there is a holding with this numeric ID in the catalog database.
    * **Not** indicates that the holding id is not in the database.
  * *Tag* : specified by the `-t` or `--tag` option.  
    * **Exists** indicates that there is a holding with this tag in the catalog database.
    * **Not** indicated that the tag is not in the database.
  * *JSON* : specified by the `j` or `--json` option.
  * *Target* : specified by the `-r` or `--target` option.
    * **Writable** indicates that the path exists and is writable by the user.
    * **Unwritable** indicates that the path exists but the user has no permission to write to it.
    * **Not** indicates that the path does not exist.
  * *File-1* : first file in the plain text file specified by the `FILELIST` argument.  
  * *File-2* : second file in the `FILELIST` plain text file.  Two files are sufficient for testing. 
    * **Exists** the file exists in the NLDS catalog.
    * **Not** the file does not exist in the NLDS catalog.
    * **regex exists** a regular expression (regex) is supplied and at least one file exists in the NLDS that matches the regex
    * **regex not** a regular expression is supplied but not files in the NLDS match the regex.

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

| *ID*      | *Label* | *HoldingID* | *Tag* |  *File-1*  |  *File-2*  |    Outcome   | Reason       |
|-----------|---------|-------------|-------|------------|------------|--------------|--------------|
| getlist_1 |    -    |     -       |   -   | **exists** | **exists** | **COMPLETE** | both files in NLDS |
| getlist_2 |    -    |     -       |   -   | **exists** | **not exists** | **COMPLETE_WITH_ERRORS** | file-1 in NLDS, file-2 not |
| getlist_3 |    -    |     -       |   -   | **not exists** | **exists** | **COMPLETE_WITH_ERRORS** | file-1 not in NLDS, file-2 in |
| getlist_4 |    -    |     -       |   -   | **not exists** | **not exists** | **FAILED** | file-1 not in NLDS, file-2 not in |
| getlist_5 | **exists** |  -       |   -   | **exists** | **exists** | **COMPLETE** | both files in holding |
| getlist_6 | **exists** |  -       |   -   | **exists** | **exists** but not in *label* | **COMPLETE_WITH_ERRORS** | only fetch the file in the holding |
| getlist_7 | **exists** |  -       |   -   | **exists** but not in *label* | **exists** | **COMPLETE_WITH_ERRORS** | only fetch the file in the holding |
| getlist_8 | **exists** |  -       |   -   | **exists** but not in *label* | **exists** but not in *label* | **FAILED** | neither file in the holding |
| getlist_9 | **NOT exists** |  -   |   -   | **exists** in NLDS | **exists** in NLDS | **FAILED** | holding not found |
| getlist_10|    -    | **exists**  |   -   | **exists** | **exists** | **COMPLETE** | both files in holding |
| getlist_11|    -    | **exists**  |   -   | **exists** | **exists** but not in *id* | **COMPLETE_WITH_ERRORS** | only fetch the file in the holding |
| getlist_12|    -    | **exists**  |   -   | **exists** but not in *id* | **exists** | **COMPLETE_WITH_ERRORS** | only fetch the file in the holding |
| getlist_13|    -    | **exists**  |   -   | **exists** but not in *id* | **exists** but not in *id* | **FAILED** | neither file in the holding |
| getlist_14|    -    | **NOT exists** | -  | **exists** in NLDS | **exists** in NLDS | **FAILED** | holding not found |
| getlist_15|    -    |   -   | **exists**  | **exists** | **exists** | **COMPLETE** | both files in holding |
| getlist_16|    -    |   -   | **exists**  | **exists** | **exists** but not in *tag* | **COMPLETE_WITH_ERRORS** | only fetch the file in the holding |
| getlist_17|    -    |   -   | **exists**  | **exists** but not in *tag* | **exists** | **COMPLETE_WITH_ERRORS** | only fetch the file in the holding |
| getlist_18|    -    |   -   | **exists**  | **exists** but not in *tag* | **exists** but not in *tag* | **FAILED** | neither file in the holding |
| getlist_19|    -    | -  | **NOT exists** | **exists** in NLDS | **exists** in NLDS | **FAILED** | holding not found |
| getlist_20| **exists** | **exists** |  -  | **exists** | **exists** | **COMPLETE** | both files in holding with *label* and *id* |
| getlist_21| **exists** | **exists** but not for *label* |  -  | **exists** | **exists** | **FAILED** | *label* and *id* must match |
| getlist_22| **exists** but not for *id* | **exists** |  -  | **exists** | **exists** | **FAILED** | *label* and *id* must match |
| getlist_23| **exists** | **exists** |  **exists** but not for *label* | **exists** | **exists** | **FAILED** | *label*, *id* and *tag* must match |
| getlist_24|     -      |     -      | - | **regex exists** |   -    | **COMPLETE** | 15 files match regex |
| getlist_25|     -      |     -      | - | **regex not**    |   -    | **FAILED**   | no files match regex |
| getlist_26| **exists** |     -      | - | **regex exists** |   -    | **COMPLETE** | 5 files match regex  |
| getlist_27| **not exists** |   -    | - | **regex exists** |   -    | **FAILED**   | label not found  |
| getlist_28| **exists** |     -      | - | **regex not**    |   -    | **FAILED**   | no files match regex  |
| getlist_29| **not exists** |   -    | - | **regex not**    |   -    | **FAILED**   | label not found  |
| getlist_30|   -    |   **exists**   | - | **regex exists** |   -    | **COMPLETE** | 5 files match regex  |
| getlist_31|   -    | **not exists** | - | **regex exists** |   -    | **FAILED**   | holding id not found  |
| getlist_32|   -    |   **exists**   | - | **regex not**    |   -    | **FAILED**   | no files match regex  |
| getlist_33|   -    | **not exists** | - | **regex not**    |   -    | **FAILED**   | no files match regex  |
| getlist_34|   _    |     -      | - | **regex exists** | **exists** | **COMPLETE** | 5 files match regex and tag |
| getlist_35|   -    |     -      | - | **regex exists** | **exists** in 2 | **COMPLETE** | 10 files match regex and tag |
| getlist_36|   -    |     -      | - | **regex exists** | **not exists** |  **FAILED** | no files match tag |
| getlist_37|   -    |     -      | - | **regex not**    | **exists** |  **FAILED** | no files match regex |
| getlist_38|   -    |     -      | - | **regex not**    | **not exists** |  **FAILED** | no files match regex |