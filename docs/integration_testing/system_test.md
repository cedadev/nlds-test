# Syatem status tests


`/system/status/` is the extention that brings up the system status web page


## Tests

| *Test ID*  | *Value* | *Colour* | Explanation |
|------------|---------|----------|-------------|
| test_monitor_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_nlds_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_catalog_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_index_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_logging_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_transfer_get_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_transfer_put_all_offline | All Consumers Offline (None running) | RED | no consumers running |
| test_nlds_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_nlds_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_nlds_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_monitor_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_monitor_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_monitor_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_catalog_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_catalog_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_catalog_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_index_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_index_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_index_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_logging_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_logging_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_logging_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_transfer_get_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_transfer_get_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_transfer_get_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_transfer_put_all_online | All Consumers Online (3/3) | GREEN | all consumers running normaly |
| test_transfer_put_all_failed | All Consumers Offline (0/3) | RED | all consumers failed to run |
| test_transfer_put_some_online | Consumers Online (2/3) | ORANGE | one consumer failed to run |
| test_faulty_rabbit_details | Login error | PURPLE | the login information on .server_config was incorrect |



test_get_success tests all services and consumers at the same time can't be tested in various states of consumers failing because the way consumers fail is built in to the code