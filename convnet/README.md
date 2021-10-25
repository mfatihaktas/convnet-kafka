# convnet

Convnet is a basic Python library to classify images with CNN.
It provides two functionalities:
* Train a basic CNN on a given data set.
* Predict the class names for a given array of images.

## Implementation
It is implemented as a single-class library.

## Installation
Navigate to the root folder, and run the following commands:

```bash
python3 setup.py bdist_wheel
pip3 install --force-reinstall dist/convnetlib-0.1.0-py3-*.whl
```

These commands are also provided in [cmd.sh](cmd.sh) for convenience.

## Usage
```python
import glob, PIL
import numpy as np
from convnetlib import convnet
from convnetlib import convnet

model = convnet.ConvNet(training_data_dir='/path/to/mnist-data/training',
						class_names=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
img_path_l = glob.glob('/path/to/imgs/*.png')
n = len(img_path_l)

plot.figure(figsize=(12, 12))
for i, img_path in enumerate(img_path_l):
  with open(img_path, 'rb') as f:
      img = PIL.Image.open(f)
      img_rgb = img.convert('RGB')
      array = np.asarray(img_rgb)
      array = np.expand_dims(array, axis=0)
      label = model.get_predicted_class_labels(array)[0]
      log(INFO, "predicted label= {}".format(label))

  plot.subplot(5, 5, i + 1)
  plot.xticks([])
  plot.yticks([])
  plot.grid(False)
  plot.imshow(np.asarray(img), cmap='gray')
  plot.xlabel(label)

plot.savefig("plot_test_results.png", bbox_inches='tight')
```

Once a `ConvNet` instance is constructed, it will check if a previously
trained model exists in `./checkpoint`. If so, the old model will be loaded. If not, a new model
will be trained over the data set in `training_data_dir`. If a new model needs to be trained
despite the presence of an old model, then `train()` should be called explicity on the model.
Note that the model in `./checkpoint` will be replaced only if the newly trained model achieves
higher accuracy than the old one.
```python
model = ConvNetModel(training_data_dir='./training', class_names=['0', '1'])
model.train()  # Will force training the model even if a previously trained model exists
```

Class labels can be got for a given (numpy) array of images, `img_array`, as:
```python
model.get_predicted_class_labels(img_array)
```

### Inputs to `ConvNet`
- `training_data_dir`: Directory for the training data set. It should be structured as

directory/<br/>
...class_a/<br/>
......a_image_1.jpg<br/>
......a_image_2.jpg<br/>
...class_b/<br/>
......b_image_1.jpg<br/>
......b_image_2.jpg<br/>
where `class_x` contain images with label `x`.
Supported image formats: `jpeg`, `png`, `bmp`, `gif`.

- `class_names`: List of class names. This list has to match the list that is found
in the training data set.

- `num_training_epochs`: Number of epochs the model will be trained for.

- `batch_size`: Number of samples to work through before updating the model parameters.

- `img_height`, `img_width`, `num_colors`: Size of every image in the data set should be the
same and be given by `height` x `width` x `colors`. The values set for these have to be consistent
with the actual image size in the data set.

See [examples/](examples/) for example(s) on how to use `ConvNet`.

## References
- https://www.tensorflow.org/tutorials/images/cnn
- https://cnvrg.io/cnn-tensorflow/
