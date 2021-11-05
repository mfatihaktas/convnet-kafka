from __future__ import annotations
import confluent_kafka, numpy
from typing import Callable

from kafkalib.debug_utils import *

## TODO: Enable setting the logging level to ERROR, INFO or WARNING

class KafkaProducer:
	def __init__(self, producer_id: str, bootstrap_servers: str,
							 handle_failed_send: Callable[[KafkaProducer, str, str, str], None], additional_conf: dict = {}):
		self.handle_failed_send = handle_failed_send
		self.conf = additional_conf
		self.conf.update(
			{'client.id': producer_id,
			 'bootstrap.servers': bootstrap_servers})
		if 'acks' not in self.conf:
			self.conf['acks'] = 1

		self.producer = confluent_kafka.Producer(self.conf)
		log(DEBUG, "constructed", producer=self)

	def __repr__(self):
		return 'KafkaProducer(conf= \n{})'.format(pprint.pformat(self.conf))

	def ack_callback(self, err, msg):
		if err is not None:
			topic, key, value = msg.topic(), msg.key(), msg.value()
			log(ERROR, "Failed to send", err=err, topic=topic, key=key, value=value)
			self.handle_failed_send(self, topic, key, value)
		else:
			log(DEBUG, "Msg sent", msg=msg)

	def send(self, topic: str, key: str, value):
		self.producer.produce(topic, key=key.encode('utf-8'), value=value, callback=self.ack_callback)
		log(DEBUG, "done", topic=topic, key=key)
