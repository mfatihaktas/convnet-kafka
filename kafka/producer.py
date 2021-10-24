import confluent_kafka

from debug_utils import *

class KafkaProducer:
	def __init__(self, producer_id: str, bootstrap_servers: str, additional_conf: dict = {}):
		self.conf = additional_conf
		self.conf.update(
			{'client.id': producer_id,
			 'bootstrap.servers': bootstrap_servers})

		self.producer = confluent_kafka.Producer(self.conf)
		log(DEBUG, "constructed", producer=self)

	def __repr__(self):
		return 'KafkaProducer(conf= \n{})'.format(pprint.pformat(self.conf))

	def ack_callback(self, err, msg):
		if err is not None:
			log(ERROR, "Failed to send", err=err, msg=msg)
		else:
			log(DEBUG, "Msg sent", msg=msg)

	def send(self, topic: str, key: str, value: str):
		self.producer.produce(topic, key.encode('utf-8'), value.encode('utf-8'), callback=self.ack_callback)
		log(DEBUG, "done", topic=topic, key=key, value=value)
