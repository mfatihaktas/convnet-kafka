import getopt, time, numpy, glob, requests
from PIL import Image
from io import BytesIO

from debug_utils import *

class ImageClient:
	def __init__(self, _id: int, img_dir: str, server_ip: str, server_port: str):
		self._id = _id
		self.img_dir = img_dir

		self.address = 'http://{}:{}'.format(server_ip, server_port)
		self.send_images()

	def send_images(self):
		log(DEBUG, "started")

		img_path_l = glob.glob(self.img_dir + '/*.png')
		for i, img_path in enumerate(img_path_l):
			log(INFO, ">> img_path= {}".format(img_path))
			log(INFO, "sleeping for 2 sec")
			time.sleep(2)
			with open(img_path, 'rb') as f:
				img = Image.open(f)
				img_rgb = img.convert('RGB')
				img_array = numpy.asarray(img_rgb)
				img_name = os.path.basename(img_path)
				log(INFO, "Sending", img_name=img_name)

				img_bytes = BytesIO()
				numpy.save(img_bytes, img_array, allow_pickle=True)
				img_bytes = img_bytes.getvalue()
				r = requests.post(self.address,
													headers={'img_name': img_name},
													data=img_bytes)
				if r.ok:
					log(INFO, "Sent", img_name=img_name, img_array_shape=img_array.shape)
				else:
					# TODO: If the post request fails, for now just simply log
					log(WARNING, "Post failed", img_name=img_name)

		log(DEBUG, "done")

def parse_argv(argv):
	m = {}
	try:
		opts, args = getopt.getopt(argv, '', ['id=', 'img-dir=', 'server-ip=', 'server-port='])
	except getopt.GetoptError:
		assert_("Wrong args")

	for opt, arg in opts:
		if opt == '--id':
			m['id'] = arg
		elif opt == '--img-dir':
			m['img_dir'] = arg
		elif opt == '--server-ip':
			m['server_ip'] = arg
		elif opt == '--server-port':
			m['server_port'] = arg
		else:
			assert_("Unexpected opt= {}, arg= {}".format(opt, arg))

	check('id' in m, "--id is required", input_args=m)
	check('img_dir' in m, "--img-dir is required", input_args=m)
	check('server_ip' in m, "--server-ip is required", input_args=m)
	check('server_port' in m, "--server-port is required", input_args=m)

	return m

if __name__ == "__main__":
	log_to_file('client.log', directory='./log')
	log_to_std()

	m = parse_argv(sys.argv[1:])
	log(DEBUG, "argv", m=m)

	client = ImageClient(
						 _id=m['id'], img_dir=m['img_dir'],
						 server_ip=m['server_ip'], server_port=m['server_port'])
