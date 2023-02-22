# Integration Testing

## Commands in the client:

  | **Command**|                                            | Tests |
  |------------|--------------------------------------------|-------|
  | all | Authentication and authorisation | [OAuth tests](./oauth_tests.md) |
  | `put`      | Put a single file.        | [Put command tests](./put_file_tests.md) |
  | `putlist`  | Put a number of files specified in a list. | [Putlist command tests](./put_filelist_tests.md)|
  | `get`      | Get a single file.                         |
  | `getlist`  | Get a number of files specified in a list. |
  | `find`     | Find and list files.                       |
  | `list`     | List holdings.                             |
  | `meta`     | Alter metadata for a holding.              |
  | `stat`     | List transactions.                         |

## Client config testing

## Requirements

  * Python 3.10+ virtual environment
  * NLDS server installed into virtual-env
  * NLDS client installed into virtual-env
  * Server config file at `/etc/nlds/server_config`
  * Client config file at `~/.nlds-config`
  * *(currently)* Access to JASMIN
  * *(currently)* A JASMIN user account
  * *(currently)* Access to the DataCore Object Storage at JASMIN
  * *(currently)* Access to the RabbitMQ server at CEDA (hosted on JASMIN)
  