# convnet-kafka

This repo implements an image classifier application. Given a directory of images (with a certain expected structure as explained below), the application will classify all the images and return the image labels.

The application consists of four components:
- `Client`: Reads the images from the given directory and sends them to the `Server`.
- `Server`: A simple http server that receives images from the `Client` and sends them to the `Kafka broker(s)`.
- `Kafka broker(s)`: Stores the images in a log data structure.
- `Classifier`: Consumes images from the `Kafka broker(s)`, predicts the class name for each and writes them back to the `Kafka broker(s)`.

## Installation
Navigate to the root folder, and run the following command:

```bash
./lib.sh install
```

## Dependencies
Can be found in [requirements.txt](requirements.txt), [convnet/requirements.txt](convnet/requirements.txt) and [kafka/requirements.txt](kafka/requirements.txt).
