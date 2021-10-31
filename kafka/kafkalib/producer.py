from __future__ import annotations
import confluent_kafka
from typing import Callable
import numpy as np

from kafkalib.debug_utils import *

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

	def send_string(self, topic: str, key: str, value: str):
		self.producer.produce(topic, key.encode('utf-8'), value.encode('utf-8'), callback=self.ack_callback)
		log(DEBUG, "done", topic=topic, key=key, value=value)

	def send_array(self, topic: str, key: str, array: np.array):
		self.producer.produce(topic, key.encode('utf-8'), array, callback=self.ack_callback)
		log(DEBUG, "done", topic=topic, key=key, array_shape=array.shape)
