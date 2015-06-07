import json
import pika
import uuid
import cpu_wmi as cpu
import dsk_wmi as disk
import mem_wmi as mem
import net_wmi as net
from system_monitor.controller import controller
from system_monitor.db import api
from system_monitor import conf
import time
import pythoncom
import socket

class Agent():
    def __init__(self, typeClass, mode):
        pythoncom.CoInitialize()    # for multi-threading
        # we take into account the hostname to allow multiple nodes to be 
        # connected at the same time
        self.typeClass = typeClass + " " + socket.gethostname()
        if typeClass[:3] == "CPU":
            self.cls = cpu.wmi_cpu(mode)
        elif typeClass[:3] == "RAM":
            self.cls = mem.wmi_mem(mode)
        elif typeClass[:4] == "DISK":
            self.cls = disk.wmi_dsk(mode)
        elif typeClass[:3] == "NET":
            self.cls = net.wmi_net(mode)
        else: 
            raise Exception('Agent not recognised!')
        self.run_agent()

    def run_agent(self):
        ag = SystemMonitorAgentAPI()
        ag.call(api.add_agent,self.typeClass)
        while (True) :
            ag.call(api.add_status,self.typeClass,self.cls.get_data())
            time.sleep(conf.update_interval)

class SystemMonitorAgentAPI(object):
    def __init__(self):
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.rpc_url))
        self._channel = self._conn.channel()

    def call(self, func, *args, **kwargs):
        body = json.dumps(
            {'func_name': func.func_name,
             'args': args,
             'kwargs': kwargs})

        self._channel.basic_publish(exchange='',
                                    routing_key='system_monitor._queue',
                                    properties=None,
                                    body=body)
