# convnet-kafka

This repo implements an image classifier application. Given a directory of images (with a certain expected structure as explained below), the application will classify all the images and return the image labels.

The application consists of four components:
- `Client`: Reads the images from the given directory and sends them to the `Server`.
- `Server`: A simple http server that receives images from the `Client` and sends them to the `Kafka broker(s)`.
- `Kafka broker(s)`: Stores the images in a log data structure.
- `Classifier`: Consumes images from the `Kafka broker(s)`, predicts the class name for each and writes them back to the `Kafka broker(s)`.

## Installation
Navigate to the root folder, and run the following command. This will build the docker image which will be used while creating the environment.

```bash
./docker.sh b
```

## Dependencies
Can be found in [requirements.txt](requirements.txt), [convnet/requirements.txt](convnet/requirements.txt) and [kafka/requirements.txt](kafka/requirements.txt).

## Usage
A basic environmen with a single `Client`, `Server`, `Kafka broker` and `Classifier` can be created locally by using [docker-compose.yml](docker-compose.yml) and [compose.sh](compose.sh).

The required container image can be created by
```bash
./docker.sh b
```

The environment can be started by
```bash
./compose.sh up
```
Note that the environment variables `TRAINING_DATA_DIR` and `CLASS_NAMES` set in [compose.sh](compose.sh) are used in [docker-compose.yml](docker-compose.yml). These should be set to appropriate values. Their role is explained later in [Inputs](inputs).

The environment can be brought down by
```bash
./compose.sh down
```

`TODO:` Environment defined in [docker-compose.yml](docker-compose.yml) is not scalable. Will write a yaml file to deploy a scalable environment on Kubernetes.

#### Notes
- `ConvNet` writes the model to `./checkpoint/` after training the model once. If the model is already available in `./checkpoint/` the next time, `ConvNet` will simply use the existing model without training a new one. One has to remove `./checkpoint/` to push `ConvNet` to train a new model. For further details, see [convnet/README.md](convnet/README.md).

### Inputs
<a name="inputs"></a>
In order to create the environment, [docker-compose.yml](docker-compose.yml) requires several environment variables to be set properly. These can be set in [compose.sh](compose.sh).

- `TRAINING_DATA_DIR`: Path to the directory that contains the images to train a convolutional neural network for classification. This sets the `training_data_dir` in `ConvNet`. Further details can be found in [convnet/README.md](convnet/README.md).

- `CLASS_NAMES`: Class names for the images. This sets the `class_names` in `ConvNet`. Further details can be found in [convnet/README.md](convnet/README.md).

- `IMG_DIR`: Path to the directory that contains the images `Client` wants to classify.
