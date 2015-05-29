import json
import pika
import uuid

from system_monitor import constants

class SystemMonitorAgentRPCAPI(object):
    def __init__(self):
        self._conn = pika.BlockingConnection(
            pika.ConnectionParameters(host=constants.rpc_url))
        self._channel = self._conn.channel()

    def call(self, func, *args, **kwargs):
        invoker = SystemMonitorRPCInvoker(self._conn, self._channel)
        return invoker.call(func, *args, **kwargs)

class SystemMonitorRPCInvoker(object):
    def __init__(self, conn, channel):
        self._conn = conn
        self._channel = channel
        result = self._channel.queue_declare(exclusive=True)
        self._callback_queue = result.method.queue

        self._channel.queue_declare(queue='system_monitor.rpc_queue')
        self._channel.basic_consume(self._on_response,
                                    no_ack=True,
                                    queue=self._callback_queue)

    def _on_response(self, ch, method, props, body):
        if self._correlation_id == props.correlation_id:
            self._response = body
            print 'got response: %s' % body   
        else:
            print 'Ignoring message w/ wrong correlation id'

    def call(self, func, *args, **kwargs):
        self._response = None
        body = json.dumps(
            {'func_name': func.func_name,
             'args': args,
             'kwargs': kwargs})
        self._correlation_id = str(uuid.uuid4())

        self._channel.basic_publish(exchange='',
                                    routing_key='system_monitor.rpc_queue',
                                    properties=pika.BasicProperties(
                                        reply_to = self._callback_queue,
                                        correlation_id = self._correlation_id),
                                    body=body)
        return self._get_result()

    def _get_result(self):
        try:
            while self._response is None:
                self._conn.process_data_events()
        except Exception:
            import pdb
            pdb.set_trace()
        return self._response