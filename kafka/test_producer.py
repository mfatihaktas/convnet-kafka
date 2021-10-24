import time, sys, getopt

from producer import KafkaProducer
from debug_utils import *

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
	check('bootstrap_servers' in m, "--bootstrap_servers is required", input_args=m)

	log(DEBUG, "done", m=m)
	return m

def test1(argv):
	log_to_std()
	m = parse_argv(argv)
	producer_id = 'p' + m['id']
	log_to_file('{}.log'.format(producer_id), directory='./log')

	producer = KafkaProducer(producer_id, m['bootstrap_servers'])
	topic = 'test'
	producer.send(topic, key=producer_id, value='v1')
	time.sleep(1)
	producer.send(topic, key=producer_id, value='v2')
	time.sleep(1)
	producer.send(topic, key=producer_id, value='v3')

	log(DEBUG, "done")

if __name__ == "__main__":
	test1(sys.argv[1:])
