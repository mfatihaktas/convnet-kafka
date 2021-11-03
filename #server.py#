import threading, queue, getopt
import numpy as np
from flask import Flask, Response

from kafkalib.producer import KafkaProducer
from debug_utils import *

def handle_failed_send(producer, topic, key, value):
	log(DEBUG, "started", topic=topic, key=key, value=value)
	producer.send(topic, key, value)

class Server_ImgsToKafka:
	def __init__(self, _id: str, kafka_bootstrap_servers: str,
							 img_height: int = 28, img_width: int = 28, num_colors: int = 3):
		self._id = _id
		self.kafka_bootstrap_servers = kafka_bootstrap_servers

		self.on = True

		self.q = queue.Queue()
		self.producer = KafkaProducer('{}_producer'.format(self._id), kafka_bootstrap_servers, handle_failed_send)
		self.topic = 'imgs'

		self.t = threading.Thread(target=self.run, daemon=True)
		self.t.start()

	def __repr__(self):
		return 'Server_ImgsToKafka(' + '\n' + \
					 '\t id= {}'.format(self._id) + '\n' + \
					 '\t kafka_bootstrap_servers= {}'.format(kafka_bootstrap_servers) + ')'

	def close(self):
		self.on = False
		log(DEBUG, "done")

	def append_to_queue(self, img_array):
		self.q.put(img_array)
		log(DEBUG, "done", img_array_shape=img_array.shape)

	def run(self):
		counter = 0
		while self.on:
			log(DEBUG, "Waiting for img_array")
			img_array = self.q.get(block=True)

			key = str(counter)
			log(INFO, "Sending to kafka", key=key, img_array_shape=img_array.shape)
			self.producer.send_array(self.topic, key, img_array)
			counter += 1
		log(DEBUG, "done")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def is_extension_allowed(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['POST'])
def index():
	if 'img' not in request.files:
		app.logger.debug("Received no image")
		return Response("POST should include field: 'img'",
										status=HTTP_400_BAD_REQUEST)

	f = request.files['img']
	if f is None or f.filename == '':
		app.logger.debug("Received empty file")
		return Response("POST should include non-empty image",
										status=HTTP_400_BAD_REQUEST)

	if not is_extension_allowed(f.filename):
		app.logger.debug("File extension not allowed; filename= {}".format(f.filename))
		return Response("File extension not allowed; {}".format(f.filename), status=400)

	img_str = f.read()
	img_array = numpy.fromstring(img_str, np.uint8)
	server.append_to_queue(img_array)
	return Response("Received; img_shape= {}".format(img_array.shape), status=201)

def parse_argv(argv):
	m = {}
	try:
		opts, args = getopt.getopt(argv, '', ['id=', 'bootstrap-servers=', 'img-height=', 'img-width=', 'num-colors='])
	except getopt.GetoptError:
		assert_("Wrong args")

	for opt, arg in opts:
		if opt == '--id':
			m['id'] = arg
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
	check('bootstrap_servers' in m, "--bootstrap-servers is required", input_args=m)

	if 'img_height' not in m:
		m['img_height'] = 28
	if 'img_width' not in m:
		m['img_width'] = 28
	if 'num_colors' not in m:
		m['num_colors'] = 3

	log(DEBUG, "done", m=m)
	return m

if __name__ == "__main__":
	log_to_file('server.log', directory='./log')
	log_to_std()

	m = parse_argv(sys.argv[1:])
	log(DEBUG, "argv", m=m)

	server = Server_ImgsToKafka(
						 _id=m['id'], kafka_bootstrap_servers=m['bootstrap_servers'],
						 img_height=m['img_height'], img_width=m['img_width'], num_colors=m['num_colors'])

	app.run(debug=True, host='0.0.0.0')
