import confluent_kafka, sys, threading, numpy, time, traceback
from typing import Callable

from kafkalib.debug_utils import *

class KafkaConsumer:
	def __init__(self, group_id: str, bootstrap_servers: str, topic_list: list[str],
							 callback_for_topic_key_value: Callable[[str, str, str], None],
							 additional_conf: dict = {}):
		self.topic_list = topic_list
		self.callback_for_topic_key_value = callback_for_topic_key_value
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

		self.consume_loop = threading.Thread(target=self.run, daemon=True)
		self.consume_loop.start()

	def __repr__(self):
		return 'KafkaConsumer(conf= \n{})'.format(pprint.pformat(self.conf))

	def wait(self):
		log(DEBUG, "started")
		self.consume_loop.join()

	def close(self):
		self.on = False
		## Close down consumer to commit final offsets.
		self.consumer.close()
		log(DEBUG, "done")

	def run(self):
		log(DEBUG, "started", topic_list=self.topic_list)
		while True:
			try:
				self.consumer.subscribe(self.topic_list)
				log(INFO, "Subscribed", topic_list=self.topic_list)
				break
			except confluent_kafka.KafkaException:
				log(WARNING, 'Topics not available, will try to subscribe again in 1 sec', topic_list=self.topic_list)
				time.sleep(1)

		while self.on:
			try:
				msg = self.consumer.poll(timeout=1.0)
				if msg is None:
					log(WARNING, "Msg is None; skipping")
					continue

				if msg.error():
					if msg.error().code() == confluent_kafka.KafkaError._PARTITION_EOF:
						## End of partition event
						log(WARNING, "Reached EOF", topic=msg.topic(), partition=msg.partition(), offset=msg.offset())
					elif msg.error():
						raise confluent_kafka.KafkaException(msg.error())
				else:
					topic = msg.topic()
					key = msg.key().decode('utf-8') if msg.key() else None
					log(DEBUG, "Got a msg", topic=msg.topic(), partition=msg.partition(), offset=msg.offset(), key=key)

					val = msg.value()
					if val is None:
						log(WARNING, "Value is None; skipping", topic=topic, key=key)
						continue
					self.callback_for_topic_key_value(topic, key, val)
			except Exception as e:
				## TODO: handle 'Subscribed topic not available' more properly
				log(WARNING, "Exception!, will go back in the consume loop after 1 sec.\n{}".format(traceback.format_exc()))
				time.sleep(1)

		log(DEBUG, "done")
