import time, sys, getopt

from consumer import KafkaConsumer
from debug_utils import *

def parse_argv(argv):
	m = {}
	try:
		opts, args = getopt.getopt(argv, '', ['id=', 'group-id=', 'bootstrap-servers='])
	except getopt.GetoptError:
		assert_("Wrong args")

	for opt, arg in opts:
		if opt == '--id':
			m['id'] = arg
		elif opt == '--group-id':
			m['group_id'] = arg
		elif opt == '--bootstrap-servers':
			m['bootstrap_servers'] = arg
		else:
			assert_("Unexpected opt= {}, arg= {}".format(opt, arg))

	check('id' in m, "--id is required", input_args=m)
	check('group_id' in m, "--group-id is required", input_args=m)
	check('bootstrap_servers' in m, "--bootstrap-servers is required", input_args=m)

	log(DEBUG, "done", m=m)
	return m

def callback_on_receive(topic: str, key: str, value: str):
	log(INFO, "Received", topic=topic, key=key, value=value)

def test1(argv):
	log_to_std()
	m = parse_argv(argv)
	consumer_id = 'c' + m['id']
	log_to_file('{}.log'.format(consumer_id), directory='./log')

	topic_l = ['test']
	consumer = KafkaConsumer(m['group_id'], m['bootstrap_servers'], topic_l, callback_on_receive)
	log(INFO, "Enter to terminate")
	input()

	log(DEBUG, "done")

if __name__ == "__main__":
	test1(sys.argv[1:])
