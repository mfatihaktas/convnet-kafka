from kafkalib.producer import KafkaProducer
from debug_utils import *

KAFKA_CONSUMER_GROUP_ID = 0
KAFKA_IMG_TOPIC = 'img'
KAFKA_CLASS_TOPIC = 'class'

def handle_failed_send(producer: KafkaProducer, topic: str, key: str, value: str):
	log(DEBUG, "Re-sending", topic=topic, key=key, value_len=len(value))
	producer.send(topic, key, value)
