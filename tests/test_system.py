import pytest


class TestSystem:
    
    def test_system_1(self):
        """test if the output for all monitor consumers online is correct"""
        time_limit = 5
        msg_dict = {"details": {"api_action": "system_stat", "target_consumer": "", "ignore_message": False}}
        
        monitor = get_consumer_status("monitor_q", "monitor", msg_dict, time_limit, 0)
        assert monitor == {"val": "All Consumers Online ("+ str(consumer_count) +"/"+ str(consumer_count) +")", "colour": "GREEN"}