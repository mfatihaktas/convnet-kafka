import glob, PIL

from debug_utils import *
from convnet_model import *

def test_w_random_imgs(model, num_imgs):
	log(INFO, "started", num_imgs=num_imgs)

	img_array = np.random.rand(num_imgs, 28, 28, 3) * 255
	class_labels = model.get_predicted_class_labels(img_array)

	log(INFO, "done", class_labels=class_labels)

def test_w_real_imgs(model, directory):
	log(INFO, "started", directory=directory)

	img_path_l = glob.glob('./imgs/*.png')
	n = len(img_path_l)

	# plot.figure(figsize=(10 * n, 10 * n))
	plot.figure(figsize=(10, 10))
	for i, img_path in enumerate(img_path_l):
		print(">> img_path= {}".format(img_path))
		with open(img_path, 'rb') as f:
			img = PIL.Image.open(f)
			img_rgb = img.convert('RGB')
			array = np.asarray(img_rgb)
			array = np.expand_dims(array, axis=0)
			label = model.get_predicted_class_labels(array)[0]
			print("label= {}".format(label))

		plot.subplot(5, 5, i + 1)
		plot.xticks([])
		plot.yticks([])
		plot.grid(False)
		plot.imshow(np.asarray(img), cmap='gray')
		plot.xlabel(label)
	# plot.show()
	plot.savefig("plot_test_w_real_imgs.png", bbox_inches='tight')
	plot.gcf().clear()

	log(INFO, "done")

if __name__ == "__main__":
	log_to_std()

	model = ConvNetModel(data_dir='/Users/mehmet/Desktop/fashion-mnist-data/training',
											 class_names=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
	# model.evaluate()

	test_w_random_imgs(model, num_imgs=10)

	test_w_real_imgs(model, 'imgs')
