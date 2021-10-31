import glob, PIL
import numpy as np
from convnetlib import convnet

from debug_utils import *

def handle_failed_write(producer, topic, key, value):
	log(DEBUG, "started", topic=topic, key=key, value=value)
	producer.send(topic, key, value)

class ImageClient:
	def __init__(self, _id: int, validation_data_dir: str, kafka_bootstrap_servers: str,
							 img_height: int = 28, img_width: int = 28, num_colors: int = 3):
		self._id = _id
		self.validation_data_dir = validation_data_dir
		self.kafka_bootstrap_servers = kafka_bootstrap_servers

		self.producer = KafkaProducer('producer_{}'.format(self._id), kafka_bootstrap_servers, handle_failed_write)

	def send_images_to_kafka(self):
		img_path_l = glob.glob(self.validation_data_dir + '/*.png')
		for i, img_path in enumerate(img_path_l):
			log(INFO, ">> img_path= {}".format(img_path))
			with open(img_path, 'rb') as f:
				img = PIL.Image.open(f)
				img_rgb = img.convert('RGB')
				img_array = np.asarray(img_rgb)
				img_name = os.path.basename()
				log(INFO, "Sending to kafka", img_name=img_name)
				self.producer.send(topic='img', key=img_name, value=img_array)
