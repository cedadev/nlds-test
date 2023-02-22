Integration Testing for NLDS
============================

This repository contains integration tests for the Near-Line Data Store (NLDS).
It requires installing and running the development versions of both the NLDS 
server and the NLDS client.
These can both be installed into a Python virtual environment, using the
`requirements.txt` in this repository:

```
python3 -m venv ~/nlds-test-venv
source ~/nlds-test-venv/bin/activate
pip install -r requirements.txt
```

Each command in the NLDS client is tested using the integration tests detailed
in the [integration test tables](./docs/integration_testing/integration_testing.md)