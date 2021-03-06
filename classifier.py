import numpy, traceback, getopt
from io import BytesIO

from kafkalib.producer import KafkaProducer
from kafkalib.consumer import KafkaConsumer
from convnetlib.convnet import ConvNet
from config import KAFKA_CONSUMER_GROUP_ID, KAFKA_IMG_TOPIC, KAFKA_CLASS_TOPIC, handle_failed_send
from debug_utils import *

class ImgClassifier:
	def __init__(self, _id, training_data_dir, class_names, bootstrap_servers,
							 img_height, img_width, num_colors):
		self._id = _id
		self.img_height = img_height
		self.img_width = img_width
		self.num_colors = num_colors

		self.on = True

		self.model = ConvNet(training_data_dir, class_names)

		self.consumer = KafkaConsumer(KAFKA_CONSUMER_GROUP_ID, bootstrap_servers,
																	[KAFKA_IMG_TOPIC], self.callback_on_receiving_img)
		self.producer = KafkaProducer('producer_at_classifier_{}'.format(_id),
																	bootstrap_servers, handle_failed_send)

	def wait(self):
		log(DEBUG, "started")
		self.consumer.wait()

	def callback_on_receiving_img(self, topic: str, key: str, value: str):
		log(DEBUG, "started", key=key, value_len=len(value))
		check(topic == KAFKA_IMG_TOPIC, "Unexpected topic", topic=topic)

		img_bytes = BytesIO(value)
		img_array = numpy.load(img_bytes, allow_pickle=True)
		log(DEBUG, "Received", img_array_shape=img_array.shape)

		img_array = numpy.expand_dims(img_array, axis=0)
		class_name = self.model.get_predicted_class_labels(img_array)[0]
		log(INFO, "Predicted", class_name=class_name)

		self.producer.send(KAFKA_CLASS_TOPIC, key, value=class_name)

		log(DEBUG, "done", key=key)

def parse_argv(argv):
	m = {}
	try:
		opts, args = getopt.getopt(argv, '', ['id=', 'training-data-dir=', 'class-names=', 'bootstrap-servers=', 'img-height=', 'img-width=', 'num-colors='])
	except getopt.GetoptError:
		assert_("Wrong args")

	for opt, arg in opts:
		if opt == '--id':
			m['id'] = arg
		elif opt == '--training-data-dir':
			m['training_data_dir'] = arg
		elif opt == '--class-names':
			try:
				m['class_names'] = arg.split(',')
			except:
				assert_("Arg --class-names is not proper; it should be a comma separated list of class names", arg_class_names=arg)
		elif opt == '--bootstrap-servers':
			m['bootstrap_servers'] = arg
		elif opt == '--img-height':
			m['img_height'] = int(arg)
		elif opt == '--img-width':
			m['img_width'] = int(arg)
		elif opt == '--num-colors':
			m['num_colors'] = int(arg)
		else:
			assert_("Unexpected opt= {}, arg= {}".format(opt, arg))

	check('id' in m, "--id is required", input_args=m)
	check('class_names' in m, "--class-names is required", input_args=m)
	check('training_data_dir' in m, "--training-data-dir is required", input_args=m)
	check('bootstrap_servers' in m, "--bootstrap-servers is required", input_args=m)

	if 'img_height' not in m:
		m['img_height'] = 28
	if 'img_width' not in m:
		m['img_width'] = 28
	if 'num_colors' not in m:
		m['num_colors'] = 3

	return m

if __name__ == "__main__":
	log_to_std()
	log_to_file('classifier.log', directory='./log')

	m = parse_argv(sys.argv[1:])
	log(DEBUG, "argv", m=m)

	classifier = ImgClassifier(m['id'], m['training_data_dir'], m['class_names'],
														 m['bootstrap_servers'], m['img_height'], m['img_width'], m['num_colors'])

	# log(INFO, "Enter to terminate")
	# input()
	classifier.wait()
