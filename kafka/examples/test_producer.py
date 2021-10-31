import time, getopt

from kafkalib.producer import KafkaProducer
from kafkalib.debug_utils import *

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

	log(DEBUG, "done", m=m)
	return m

def handle_failed_send(producer, topic, key, value):
	log(DEBUG, "started", topic=topic, key=key, value=value)
	producer.send_string(topic, key, value)

def test1(argv):
	log_to_std()
	m = parse_argv(argv)
	producer_id = 'p' + m['id']
	log_to_file('{}.log'.format(producer_id), directory='./log')

	producer = KafkaProducer(producer_id, m['bootstrap_servers'], handle_failed_send)
	topic, key = 'test', producer_id
	producer.send_string(topic, key, value='v1')
	time.sleep(1)
	producer.send_string(topic, key, value='v2')
	time.sleep(1)
	producer.send_string(topic, key, value='v3')

	log(DEBUG, "done")

if __name__ == "__main__":
	test1(sys.argv[1:])
