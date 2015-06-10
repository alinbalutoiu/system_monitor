import pika
import json

from system_monitor import conf
from system_monitor.db import api as db_api
from system_monitor.db import models


class SystemMonitorControllerAPI(object):
    def __init__(self):
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=conf.host_url))
        self._channel = self._conn.channel()
        self._channel.queue_declare(queue='system_monitor._queue')
        self._channel.basic_consume(self._on_request,
                                    queue='system_monitor._queue')

    def _on_request(self, ch, method, props, body):
        req = json.loads(body)

        agent_name = req['agent_name']
        args = req['args']
        kwargs = req['kwargs']

        try:
            db_api.add_agent(agent_name)
            db_api.add_status(agent_name, *args, **kwargs)
        except Exception as exc:
            pass

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def accept(self):
        self._channel.start_consuming()
