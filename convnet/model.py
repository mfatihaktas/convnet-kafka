"""
Refs:
-- https://www.tensorflow.org/tutorials/keras/save_and_load
-- https://cnvrg.io/cnn-tensorflow/
"""

import os
import tensorflow as tf
import numpy as np

from debug_utils import *
from plot_utils import *

SEED = 123

class ConvNetModel:
	def __init__(self, data_dir: str, class_names: list, num_training_epochs: int = 1,
							 batch_size: int = 32, img_height: int = 28, img_width: int = 28, num_colors: int = 3, max_pixel_value: int = 255):
		self.data_dir = data_dir
		self.num_training_epochs = num_training_epochs
		self.class_names = class_names
		self.batch_size = batch_size
		self.img_height = img_height
		self.img_width = img_width
		self.num_colors = num_colors
		self.max_pixel_value = max_pixel_value

		self.num_classes = len(self.class_names)
		check(os.path.exists(self.data_dir), "Non-existing directory", data_dir=self.data_dir)

		self.train_dataset = None
		self.validation_dataset = None

		# self.checkpoint_path = 'checkpoint/cp.ckpt'
		self.checkpoint_path = './checkpoint/cp.ckpt'
		# self.checkpoint_dir = os.path.dirname('checkpoint')

		self.model = self.load()
		if self.model is None:
			self.model = self.train()

	def __repr__(self):
		return 'ConvNetModel(\n' + \
					 '	data_dir= {}'.format(self.data_dir) + '\n' + \
					 '	num_training_epochs= {}'.format(self.num_training_epochs) + '\n' + \
					 '	batch_size= {}'.format(self.batch_size) + '\n' + \
					 '	img_height= {}'.format(self.img_height) + '\n' + \
					 '	img_width= {}'.format(self.img_width) + '\n)'

	def summary(self):
			self.model.summary()

	def create_model(self):
		layer_l = [tf.keras.layers.experimental.preprocessing.Rescaling(1. / self.max_pixel_value),
							 tf.keras.layers.Conv2D(32, kernel_size=(3,3), padding='same', activation="relu", input_shape=(self.img_height, self.img_width, self.num_colors)),
							 tf.keras.layers.MaxPooling2D((2, 2), strides=2),
							 tf.keras.layers.Conv2D(64, kernel_size=(3,3), padding='same', activation="relu"),
							 tf.keras.layers.MaxPooling2D((2, 2), strides=2),
							 tf.keras.layers.Flatten(),
							 tf.keras.layers.Dense(100, activation="relu"),
							 tf.keras.layers.Dropout(0.2),
							 tf.keras.layers.Dense(self.num_classes, activation="softmax")]

		return tf.keras.Sequential(layer_l)

	def load_data(self):
		## TODO: Catch any error and crash gracefully
		if self.train_dataset is None:
			self.train_dataset = tf.keras.utils.image_dataset_from_directory(
														 self.data_dir,
														 batch_size=self.batch_size,
														 image_size=(self.img_height, self.img_width),
														 validation_split=0.2,
														 subset='training',
														 seed=SEED)
			log(DEBUG, "Loaded training dataset", class_names=self.train_dataset.class_names)

		if self.validation_dataset is None:
			self.validation_dataset = tf.keras.utils.image_dataset_from_directory(
				                          self.data_dir,
				                          batch_size=self.batch_size,
				                          image_size=(self.img_height, self.img_width),
				                          validation_split=0.2,
				                          subset='validation',
				                          seed=SEED)
			log(DEBUG, "Loaded validation dataset", class_names=self.validation_dataset.class_names)

		check(self.num_classes == len(self.train_dataset.class_names) and \
					all(self.class_names[i] == self.train_dataset.class_names[i] for i in range(self.num_classes)),
					"Input class_names does not match with what is found in data",
					input_class_names=self.class_names, found_class_names=self.train_dataset.class_names)
		log(DEBUG, "done")

	def train(self, num_epoch=1):
		log(DEBUG, "started")

		self.load_data()

		model = self.create_model()
		model.compile(optimizer='adam',
									loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
									metrics=['accuracy'])

		## TODO: Get back to patience
		callback_l = [tf.keras.callbacks.EarlyStopping(patience=5),
									tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path, save_best_only=True, verbose=1)]
		history = model.fit(self.train_dataset,
												epochs=num_epoch,
												validation_data=self.validation_dataset,
												callbacks=callback_l)

		loss, accuracy = model.evaluate(self.validation_dataset)
		log(INFO, "Training is finished; results on validation dataset:", loss=loss, accuracy=accuracy, history=history)

		fontsize = 14
		fig, axs = plot.subplots(1, 2)
		figsize = (2*5, 5)

		ax = axs[0]
		plot.sca(ax)
		plot.plot(history.history['accuracy'], label='Training', color=next(nice_color), marker=next(marker_cycle), linestyle=next(linestyle_cycle), mew=3, ms=5)
		plot.plot(history.history['val_accuracy'], label='Validation', color=next(nice_color), marker=next(marker_cycle), linestyle=next(linestyle_cycle), mew=3, ms=5)
		plot.ylabel('Accuracy', fontsize=fontsize)
		plot.xlabel('Epoch', fontsize=fontsize)
		plot.legend(fontsize=fontsize)

		ax = axs[1]
		plot.sca(ax)
		plot.plot(history.history['loss'], label='Training', color=next(nice_color), marker=next(marker_cycle), linestyle=next(linestyle_cycle), mew=3, ms=5)
		plot.plot(history.history['val_loss'], label='Validation', color=next(nice_color), marker=next(marker_cycle), linestyle=next(linestyle_cycle), mew=3, ms=5)
		plot.ylabel('Loss', fontsize=fontsize)
		plot.xlabel('Epoch', fontsize=fontsize)
		plot.legend(fontsize=fontsize)

		fig.set_size_inches(figsize[0], figsize[1] )
		plot.subplots_adjust(hspace=0.25, wspace=0.25)
		plot.savefig('plot_accuracy_loss_over_epochs.png', bbox_inches='tight')

		log(DEBUG, "done")
		return model

	def evaluate(self):
		self.load_data()
		loss, accuracy = self.model.evaluate(self.validation_dataset)
		log(INFO, "done", loss=loss, accuracy=accuracy)

	def load(self):
		if not os.path.exists(self.checkpoint_path):
			log(WARNING, 'Does not exist', checkpoint_path=self.checkpoint_path)
			return None

		## TODO: Check if it is better to do this with tf.keras.models.load_model
		return tf.keras.models.load_model(self.checkpoint_path)

	def sample_from_validation_dataset(self, num_samples):
		# return self.validation_dataset.take(num_samples).as_numpy()
		# return np.asarray(list(self.validation_dataset.shuffle(num_samples).take(num_samples)))
		# l = list(self.validation_dataset.shuffle(num_samples).take(num_samples).as_numpy_iterator())

		# l = []
		# for d in self.validation_dataset:
		# 	print("d= {}".format(d))
		# 	if len(l) < 1:
		# 		l.append(d[0].numpy)
		# 	else:
		# 		break
		# log(WARNING, "", l=l)
		# return np.ndarray(l)

		return np.stack(list(self.validation_dataset))

	def get_predicted_class_labels(self, img_array: np.ndarray) -> np.ndarray:
		r = []
		for i in np.argmax(self.model.predict(img_array), axis=1):
			r.append(self.class_names[i])
		return r

if __name__ == "__main__":
	log_to_std()

	model = ConvNetModel(data_dir='/Users/mehmet/Desktop/fashion-mnist-data/training',
											 class_names=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

	# img_array = model.sample_from_validation_dataset(num_samples=10)
	img_array = np.random.rand(10, 28, 28, 3) * 255
	# log(INFO, "", img_array=img_array)
	class_label_l = model.get_predicted_class_labels(img_array)
	log(INFO, "Result for random images", class_label_l=class_label_l)

	img_array = np.random.rand(10, 28, 28, 3) * 255

	model.evaluate()
