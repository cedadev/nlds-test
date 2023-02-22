OAuth tests
===========

Each command relies on the user being authenticated via OAuth.  This code is 
common for each command so can either be tested just once, using a single 
command such as `list` or `stat`, or when each command is invoked separately.
The command line options are:

  * `-u, --user`
  * `-g, --group`

Variables:
----------

  * *User* : the user name.  Specified by `-u`, `--user` or in the `default_user` 
  field in the `~/.nlds-config` file.
  * *Group* : the group name.  Specified by `-g`, `--group` or in the `default_group`
  field in the `~/.nlds-config` file.
  * `~/.nlds-token` : the file containing the OAuth token.
  * *Password* : user is prompted for a password if the `~/.nlds-token` file 
  doesn't exist.

Tests
-----

  | command line | *User* | *Group* | `~/.nlds-token` | *Password* | Expected outcome |
  |--------------|------|-------|-----------------|----------|------------------|
  | `-u, --user `            | NOT **exist**| N/A | NOT **exist** | N/A | User is asked for password. Fetching OAuth token fails. Authentication fails. |
  |                        | NOT **exist**| N/A | **exists** | N/A | Authentication fails. |
  |                        | **exists**| N/A | NOT **exist** | Requested, correct | Fetching OAuth token succeeds. Token file is created. Authentication succeeds |
  |                        | **exists**| N/A | NOT **exist** | Requested, incorrect | Authentication fails |
  |                        | **exists**| N/A | corrupted | N/A | Authentication fails. |
  |                        | **exists**| N/A | contains expired token. | N/A | Fetching refreshed token succeeds. Token file is overwritten. Authentication succeeds. |
  | `-g, --group`            | N/A | NOT **exist** | N/A | N/A| Authentication fails. |
  |                        | NOT a member of group | **exists** | N/A | N/A |Authentication fails. |
  |                        | member of the group | **exists** | N/A | N/A | Authentication succeeds. |

  [return](./integration_testing.md)