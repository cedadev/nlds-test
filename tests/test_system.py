import pytest
import asyncio
import time
import requests
# import json

import jinja2.environment
from fastapi import Request
from requests.auth import HTTPBasicAuth
import abc
from fastapi.responses import RedirectResponse

# from nlds.rabbit import rpc_publisher
from tests.conftest import loop, pause_fixture, monitor_fixture_3, \
worker_fixture_3, logger_fixture_3, put_transfer_fixture_3, \
get_transfer_fixture_3, catalog_fixture_get_3, index_fixture_3

from nlds.routers import system



@pytest.mark.usefixtures("loop", "pause_fixture")
class TestSystem1:
    def test_monitor_all_offline(self, loop):
        """testing monitor offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "monitor_q", "monitor", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
        
        
    def test_nlds_all_offline(self, loop):
        """testing nlds offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "nlds_q", "nlds", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
        
        
    def test_catalog_all_offline(self, loop):
        """testing catalog offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "catalog_q", "catalog", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
        
        
    def test_index_all_offline(self, loop):
        """testing index offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "index_q", "index", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
        
        
    def test_logging_all_offline(self, loop):
        """testing logging offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "logging_q", "logging", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
        
        
    def test_transfer_get_all_offline(self, loop):
        """testing transfer_get offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_get_q", "transfer_get", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
        
        
    def test_transfer_put_all_offline(self, loop):
        """testing transfer_put offline"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_put_q", "transfer_put", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Offline (None running)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (None running)"
        assert consumer["colour"] == "RED"
    


@pytest.mark.usefixtures("loop", "pause_fixture", "monitor_fixture_3", 
                         "worker_fixture_3", "logger_fixture_3", 
                         "put_transfer_fixture_3", "get_transfer_fixture_3", 
                         "catalog_fixture_get_3", "index_fixture_3")
class TestSystem2:
    
    def test_nlds_all_online(self, index_fixture_3, loop):
        """testing if nlds works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "nlds_q", "nlds", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_nlds_all_failed(self, index_fixture_3, loop):
        """testing all nldss fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "nlds_q", "nlds", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_nlds_some_online(self, index_fixture_3, loop):
        """testing some nldss work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "nlds_q", "nlds", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"
        
        
    
    def test_monitor_all_online(self, monitor_fixture_3, loop):
        """testing if monitor works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "monitor_q", "monitor", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_monitor_all_failed(self, monitor_fixture_3, loop):
        """testing all monitors fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "monitor_q", "monitor", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_monitor_some_online(self, monitor_fixture_3, loop):
        """testing some monitors work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "monitor_q", "monitor", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"
        
        
        
    def test_catalog_all_online(self, catalog_fixture_get_3, loop):
        """testing if catalog works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "catalog_q", "catalog", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_catalog_all_failed(self, catalog_fixture_get_3, loop):
        """testing all catalogs fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "catalog_q", "catalog", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_catalog_some_online(self, catalog_fixture_get_3, loop):
        """testing some catalogs work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "catalog_q", "catalog", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"
        
        

    def test_index_all_online(self, index_fixture_3, loop):
        """testing if index works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "index_q", "index", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_index_all_failed(self, index_fixture_3, loop):
        """testing all indexs fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "index_q", "index", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_index_some_online(self, index_fixture_3, loop):
        """testing some indexs work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "index_q", "index", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"
        
        
    
    def test_logging_all_online(self, logger_fixture_3, loop):
        """testing if logging works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "logging_q", "logging", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_logging_all_failed(self, logger_fixture_3, loop):
        """testing all loggings fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "logging_q", "logging", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_logging_some_online(self, logger_fixture_3, loop):
        """testing some loggings work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "logging_q", "logging", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"
        
        
        
    def test_transfer_get_all_online(self, get_transfer_fixture_3, loop):
        """testing if transfer_get works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_get_q", "transfer_get", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_transfer_get_all_failed(self, get_transfer_fixture_3, loop):
        """testing all transfer_gets fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_get_q", "transfer_get", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_transfer_get_some_online(self, get_transfer_fixture_3, loop):
        """testing some transfer_gets work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_get_q", "transfer_get", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"
        
        
        
    def test_transfer_put_all_online(self, put_transfer_fixture_3, loop):
        """testing if transfer_put works"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_put_q", "transfer_put", msg_dict, time_limit, 0))
        consumer = consumer[0]
        
        assert consumer == {"val": "All Consumers Online (3/3)", 
                            "colour": "GREEN"}
        assert consumer["val"] == "All Consumers Online (3/3)"
        assert consumer["colour"] == "GREEN"
        
    
    def test_transfer_put_all_failed(self, put_transfer_fixture_3, loop):
        """testing all transfer_puts fail"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_put_q", "transfer_put", msg_dict, time_limit, 3))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "All Consumers Offline (0/3)", 
                            "colour": "RED"}
        assert consumer["val"] == "All Consumers Offline (0/3)"
        assert consumer["colour"] == "RED"
        
        
    def test_transfer_put_some_online(self, put_transfer_fixture_3, loop):
        """testing some transfer_puts work"""
        
        time_limit = 5
        msg_dict = {
            "details": {
                "api_action": "system_stat", 
                "target_consumer": "", 
                "ignore_message": False
                }
            }
        
        consumer = loop.run_until_complete(
            system.get_consumer_status(
                "transfer_put_q", "transfer_put", msg_dict, time_limit, 1))
        consumer = consumer[0]
        
        consumer.pop("failed")
        
        assert consumer == {"val": "Consumers Online (2/3)", 
                            "colour": "ORANGE"}
        assert consumer["val"] == "Consumers Online (2/3)"
        assert consumer["colour"] == "ORANGE"



    def test_get_success(self, loop, monitor_fixture_3, worker_fixture_3, 
                         logger_fixture_3, put_transfer_fixture_3, 
                         get_transfer_fixture_3, catalog_fixture_get_3, 
                         index_fixture_3):
        """test if every consumer in get works """
        
        # uses a pytest fixture to make an event loop that will run the asyncronus
        # function that is being called and store its output
        get = loop.run_until_complete(system.get(Request))
        
        # gets the output as a dict to be easily manipulated
        attrs = (get.__dict__)
        
        # removes dictionary entries that would be too difficult to consistently test
        # e.g: HTML code that will keep updating
        attrs.pop('background')
        attrs.pop('body')
        attrs.pop('raw_headers')
        
        to_assert = ("{'template': <Template 'index.html'>, "
"'context': {'request': <class 'starlette.requests.Request'>, 'stats': "
"{'monitor': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'catalog': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'nlds_worker': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'index': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'get_transfer': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'put_transfer': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'logger': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, 'failed': "
"{'failed_num': 0, 'failed_colour': 'alert-success'}}}, 'status_code': 200}")
    
    
        status = ("{'monitor': {'val': 'All Consumers Online (3/3)', "
"'colour': 'GREEN'}, "
"'catalog': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'nlds_worker': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'index': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'get_transfer': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'put_transfer': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, "
"'logger': {'val': 'All Consumers Online (3/3)', 'colour': 'GREEN'}, 'failed': "
"{'failed_num': 0, 'failed_colour': 'alert-success'}}")
    
        assert str(attrs) == to_assert
        
        assert "template" in attrs
        
        assert isinstance(attrs["template"], jinja2.environment.Template)

        assert attrs["status_code"] == 200
        
        assert isinstance(attrs["context"]["request"], abc.ABCMeta)
        
        assert str(attrs["context"]["stats"]) == status


    def test_faulty_rabbit_details(self, index_fixture_3, loop):
        # tests what happens if rabbits is given faulty login and password info
        
        user = "rabbit"
        password = "password"
        
        success = {"val": ("Login error"), "colour": "PURPLE"}
        
        try:
            consumer_tags = (system.get_consumer_info("130.246.3.98", "15672", 
                    "index_q", user, password, "system-monitoring-development"))
            val = "test failed"
            
        except system.LoginError as e:
            print("Your RabbitMQ login information is incorrect or not authorised ")
            print("Please enter valid login information in the JASMIN .server_config file ")
            val = {
                "val": ("Login error"), 
                "colour": "PURPLE"
                }
            
        assert success == val
            
            
            
            
            
    def test_get_service_json_success(self, loop, monitor_fixture_3, worker_fixture_3, 
                         logger_fixture_3, put_transfer_fixture_3, 
                         get_transfer_fixture_3, catalog_fixture_get_3, 
                         index_fixture_3):
        """test if every consumer in get works """
        
        # uses a pytest fixture to make an event loop that will run the asyncronus
        # function that is being called and store its output
        get = loop.run_until_complete(system.get_service_json(Request, "monitor", 3))
        
        
        
        del get["pid"]
        del get["hostname"]
    
        assert {"microservice_name":"monitor",
            "total_num":3,
            "num_failed":0,
            "num_success":3,
            "failed_list":[]} == get
        
        
        
        
    def test_get_service_json_fail(self, loop, monitor_fixture_3, worker_fixture_3, 
                         logger_fixture_3, put_transfer_fixture_3, 
                         get_transfer_fixture_3, catalog_fixture_get_3, 
                         index_fixture_3):
        """test if every consumer in get works """
        
        # uses a pytest fixture to make an event loop that will run the asyncronus
        # function that is being called and store its output
        get = loop.run_until_complete(system.get_service_json(Request, "aihdsgi", 3))
        
        print(get)
    
        assert isinstance(get, RedirectResponse)