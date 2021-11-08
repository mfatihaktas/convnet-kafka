import numpy, threading, queue, getopt
from flask import Flask, request, Response

from kafkalib.producer import KafkaProducer
from config import KAFKA_IMG_TOPIC, handle_failed_send
from debug_utils import *
from config import ALLOWED_IMG_EXTENSIONS

class Server_ImgsToKafka:
	def __init__(self, _id: str, kafka_bootstrap_servers: str):
		self._id = _id
		self.kafka_bootstrap_servers = kafka_bootstrap_servers

		self.on = True

		self.q = queue.Queue()
		self.producer = KafkaProducer('{}_producer'.format(self._id), kafka_bootstrap_servers, handle_failed_send)

		self.t = threading.Thread(target=self.run, daemon=True)
		self.t.start()

	def __repr__(self):
		return 'Server_ImgsToKafka(' + '\n' + \
					 '\t id= {}'.format(self._id) + '\n' + \
					 '\t kafka_bootstrap_servers= {}'.format(kafka_bootstrap_servers) + ')'

	def close(self):
		self.on = False
		log(DEBUG, "done")

	def append_to_queue(self, img_name, img_bytes):
		self.q.put((img_name, img_bytes))
		log(DEBUG, "Appended", img_name=img_name)

	def run(self):
		counter = 0
		while self.on:
			log(DEBUG, "Waiting for img-{}".format(counter))
			img_name, img_bytes = self.q.get(block=True)

			log(INFO, "Sending to kafka", img_name=img_name)

			# self.producer.send(KAFKA_IMG_TOPIC, key=img_name, value=img_array.tobytes())
			self.producer.send(KAFKA_IMG_TOPIC, key=img_name, value=img_bytes)
			counter += 1
		log(DEBUG, "done")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)

def is_extension_allowed(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS

@app.route('/', methods=['POST'])
def index():
	img_name = request.headers['img_name']
	log(DEBUG, "started", img_name=img_name)
	if not is_extension_allowed(img_name):
		app.logger.debug("File extension not allowed; img_name= {}".format(img_name))
		return Response("File extension not allowed; img_name= {}".format(img_name), status=400)

	img_bytes = numpy.array(request.get_data())
	server.append_to_queue(img_name, img_bytes)
	return Response("Received; img_name= {}".format(img_name), status=201)

def parse_argv(argv):
	m = {}
	try:
		opts, args = getopt.getopt(argv, '', ['id=', 'bootstrap-servers='])
	except getopt.GetoptError:
		assert_("Wrong args")

	for opt, arg in opts:
		if opt == '--id':
			m['id'] = arg
		elif opt == '--bootstrap-servers':
			m['bootstrap_servers'] = arg
		else:
			assert_("Unexpected opt= {}, arg= {}".format(opt, arg))

	check('id' in m, "--id is required", input_args=m)
	check('bootstrap_servers' in m, "--bootstrap-servers is required", input_args=m)

	return m

if __name__ == "__main__":
	log_to_file('server.log', directory='./log')
	log_to_std()

	m = parse_argv(sys.argv[1:])
	log(DEBUG, "argv", m=m)

	server = Server_ImgsToKafka(_id=m['id'], kafka_bootstrap_servers=m['bootstrap_servers'])

	app.run(debug=True, host='0.0.0.0')
