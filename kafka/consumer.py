import confluent_kafka, sys, threading
from typing import Callable

from debug_utils import *

class KafkaConsumer:
	def __init__(self, group_id: str, bootstrap_servers: str, topic_list: list[str],
							 msg_callback: Callable[[str, str, str], None], additional_conf: dict = {}):
		self.topic_list = topic_list
		self.msg_callback = msg_callback
		self.conf = additional_conf
		self.conf.update(
			{'group.id': group_id,
			 'bootstrap.servers': bootstrap_servers})
		if 'auto.offset.reset' not in self.conf:
			# self.conf['auto.offset.reset'] = 'earliest'
			self.conf['auto.offset.reset'] = 'smallest'

		self.on = True

		self.consumer = confluent_kafka.Consumer(self.conf)
		log(DEBUG, "constructed", consumer=self)

		self.t = threading.Thread(target=self.run, daemon=True)
		self.t.start()

	def __repr__(self):
		return 'KafkaConsumer(conf= \n{})'.format(pprint.pformat(self.conf))

	def close(self):
		self.on = False
		log(DEBUG, "done")

	def run(self):
		log(DEBUG, "started", topic_list=self.topic_list)
		try:
			self.consumer.subscribe(self.topic_list)
			while self.on:
				msg = self.consumer.poll(timeout=1.0)
				if msg is None:
					continue

				sys.stdout.flush()

				if msg.error():
					if msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
						## End of partition event
						log(WARNING, "Reached EOF", topic=msg.topic(), partition=msg.partition(), offset=msg.offset())
					elif msg.error():
						raise confluent_kafka.KafkaException(msg.error())
				else:
					key = msg.key().decode('utf-8') if msg.key() else None
					log(DEBUG, "Got a msg", topic=msg.topic(), partition=msg.partition(), offset=msg.offset(), key=key)
					self.msg_callback(msg.topic(), key, msg.value().decode('utf-8'))

				sys.stdout.flush()
		finally:
			## Close down consumer to commit final offsets.
			self.consumer.close()

		log(DEBUG, "done")
