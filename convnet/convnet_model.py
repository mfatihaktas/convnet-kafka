"""
Refs:
-- https://www.tensorflow.org/tutorials/images/cnn
-- https://cnvrg.io/cnn-tensorflow/

class ConvNetModel: Implements a basic convolutional network model to learn how to
classify images.

Inputs:
* training_data_dir: Directory of the training data set. It should be structured as
directory/
...class_a/
......a_image_1.jpg
......a_image_2.jpg
...class_b/
......b_image_1.jpg
......b_image_2.jpg
where folder class_x contain images with label x.
Supported image formats: jpeg, png, bmp, gif

* class_names: List of class names. This list has to match the list that is found
in the training data set.

* num_training_epochs: Number of epochs the model will be trained for.

* batch_size: Number of samples to work through before updating the model parameters.

* img_height, img_width, num_colors: Size of every image in the data set should be the
same and be given by height x width x colors. The values set for these have to be consistent
with the actual image size in the data set.

How to use?
Once an instance of ConvNetModel has been constructed, it will check if a previously
trained model exists in ./checkpoint. If so, the old model will be loaded. If not, a new model
will be trained over the data set in ./training_data_dir. If a new model needs to be trained
despite the presence of an old model, then train() should be called explicity on the model.
Note that the model in ./checkpoint will be replaced only if the newly trained model achieves
higher accuracy than the old one.
E.g.,
model = ConvNetModel(training_data_dir='./training', class_names=['0', '1'])
model.train()	 # Will force training the model even if a previously trained model exists

Class labels can be got for a given (numpy) array of images, img_array, as:
model.get_predicted_class_labels(img_array)

See test.py for example(s) on how to use ConvNetModel.

To install dependencies, do
./run.sh i

To setup a virtual environment, do
$ python3 -m venv ./venv
To start the virtual environment, do
$ source run.sh s

TODO: Should we ship this in a container?
"""

import os
import tensorflow as tf
import numpy as np

from debug_utils import *
from plot_utils import *

SEED = 123
MAX_PIXEL_VALUE = 255

class ConvNetModel:
	def __init__(self, training_data_dir: str, class_names: list, num_training_epochs: int = 1,
							 batch_size: int = 32, img_height: int = 28, img_width: int = 28, num_colors: int = 3):
		self.training_data_dir = training_data_dir
		self.num_training_epochs = num_training_epochs
		self.class_names = class_names
		self.batch_size = batch_size
		self.img_height = img_height
		self.img_width = img_width
		self.num_colors = num_colors
		self.MAX_PIXEL_VALUE = MAX_PIXEL_VALUE

		self.num_classes = len(self.class_names)
		check(os.path.exists(self.training_data_dir),
					"Non-existing directory", training_data_dir=self.training_data_dir)

		self.train_dataset = None
		self.validation_dataset = None

		self.checkpoint_path = './checkpoint/cp.ckpt'
		if not os.path.exists(self.checkpoint_path):
			os.makedirs(self.checkpoint_path)

		self.model = self.load()
		if self.model is None:
			self.model = self.train()

	def __repr__(self):
		return 'ConvNetModel(\n' + \
					 '	training_data_dir= {}'.format(self.training_data_dir) + '\n' + \
					 '	num_training_epochs= {}'.format(self.num_training_epochs) + '\n' + \
					 '	batch_size= {}'.format(self.batch_size) + '\n' + \
					 '	img_height= {}'.format(self.img_height) + '\n' + \
					 '	img_width= {}'.format(self.img_width) + '\n)'

	def summary(self):
			self.model.summary()

	def create_model(self):
		layer_l = [tf.keras.layers.experimental.preprocessing.Rescaling(1. / self.MAX_PIXEL_VALUE),
							 tf.keras.layers.Conv2D(32, kernel_size=(3,3), padding='same', activation="relu",
																			input_shape=(self.img_height, self.img_width, self.num_colors)),
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
														 self.training_data_dir,
														 batch_size=self.batch_size,
														 image_size=(self.img_height, self.img_width),
														 validation_split=0.2,
														 subset='training',
														 seed=SEED)
			log(DEBUG, "Loaded training dataset", class_names=self.train_dataset.class_names)

		if self.validation_dataset is None:
			self.validation_dataset = tf.keras.utils.image_dataset_from_directory(
																	self.training_data_dir,
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
		try:
			return tf.keras.models.load_model(self.checkpoint_path)
		except OSError:
			log(WARNING, 'Saved model does not exist', checkpoint_path=self.checkpoint_path)
			return None

	def get_predicted_class_labels(self, img_array: np.ndarray) -> np.ndarray:
		r = []
		for i in np.argmax(self.model.predict(img_array), axis=1):
			r.append(self.class_names[i])
		return r
