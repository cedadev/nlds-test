# Get command tests

`get` is the command that enables users to get a single file from the NLDS.
The `-u, --user` and `-g, --group` command line arguments are tested by the
[OAuth tests](./oauth_tests.md).  
The other command line options and arguments are:

  * `-l, --label` : the label of a holding to add files to.
  * `-b, --job_label` : the label to give the put job so the user can track progress.
  * `-i, --holding_id` : the numeric id of a holding to add files to.
  * `-t, --tag` : the tag of a holding to add files to.
  * `-j, --json` : return the output as JSON
  * `-r, --target` : the target path for the retrieved file.  Default is to
  retrieve the file to its original path.
  * `FILEPATH` : the path of the file to put to the NLDS.

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
  * *File* : specified by the `FILEPATH` argument.  
    * **Exists** the file exists in the NLDS catalog.
    * **Not** the file does not exist in the NLDS catalog.

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
| get_1 |    -    |     -      |     -       |   -   | **exists** | **COMPLETE** | file in NLDS |
| get_2 |    -    |     -      |     -       |   -   | **NOT exists** | **FAILED** | file not in NLDS |
| get_3 | **exists** |  -      |     -       |   -   | **exists** | **COMPLETE** | file in holding with label |
| get_4 | **exists** |  -      |     -       |   -   | **NOT exists** | **FAILED** | file not in holding |
| get_5 | **exists** |  -      |     -       |   -   | **exists** but not in holding | **FAILED** | file not in holding |
| get_6 |    -    |     -      | **exists**  |   -   | **exists** | **COMPLETE** | file in holding |
| get_7 |    -    |     -      | **exists**  |   -   | **NOT exists** | **FAILED** | file not in holding |
| get_8 |    -    |     -      | **NOT exists**  |   -   | **exists** | **FAILED** | holding not found |
| get_9 |    -    |     -      | **NOT exists**  |   -   | **NOT exists** | **FAILED** | holding not found |
| get_10 |   -    | **NOT exists** |     -       |   -   | **exists** | **COMPLETE** | job label created |
| get_11 |   -    | **exists** |         -       |   -   | **exists** | **COMPLETE** | two identical job labels created |
| get_12 |   -    |     -      |      -      | **exists** | **exists** | **COMPLETE** | file in holding with tag |
| get_13 |   -    |     -      |      -      | **NOT exists** | **exists** | **FAILED** | file exists but not in holding with tag |
| get_14 |   -    |     -      |      -      | **exists** | **NOT exists** | **FAILED** | file does not exist but tag exists in a holding |
| get_15 | **exists** | -      |      -      | **exists** | **exists** | **COMPLETE** | file and tag exists in holding with label |
| get_16 | **exists** | -      |      -      | **NOT exists** | **exists** | **FAILED** | file exists in holding with label, tag does not. label and tag must match |
| get_17 | **NOT exists** | -      |      -      | **exists** | **exists** | **FAILED** | file exists in holding with tag, label does not. label and tag must match |
| get_18 |   -    |     -      | **exists**  | **exists** | **exists** | **COMPLETE** | file and tag exists in holding with id |
| get_19 |   -    |     -      | **exists**  | **NOT exists** | **exists** | **FAILED** | file exists in holding with id, tag does not. id and tag must match |
| get_20 |   -    |     -      | **NOT exists** | **exists** | **exists** | **FAILED** | file exists in holding with tag, holding id does not. id and tag must match |
 [return](./integration_testing.md)