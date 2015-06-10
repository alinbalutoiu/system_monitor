import wmi
import pika
import json
import time

from system_monitor import conf
from system_monitor.db import api


class Agent_Model():
    def __init__(self):
        self.conn = wmi.WMI()
        self.data = {}

    # each agent provides it's own implementation
    def setData(self):
        pass

    # each agent provides it's own implementation
    def setAgentName(self):
        self.agent_name = 'Test'

    def start_agent(self):
        self.setAgentName()
        ag = SendMessage(self.agent_name)
        while (True):
            self.setData()
            ag.upload_data(self.data)
            time.sleep(conf.update_interval)


class SendMessage(object):
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(host = conf.host_url))
        self._channel = self._conn.channel()

    def upload_data(self, *args, **kwargs):
        body = json.dumps(
            {'agent_name': self.agent_name,
             'args': args,
             'kwargs': kwargs})

        self._channel.basic_publish(exchange='',
                                    routing_key='system_monitor._queue',
                                    properties=None,
                                    body=body)
