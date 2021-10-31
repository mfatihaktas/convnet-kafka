# convnet-kafka

This repo implements an image classifier application. Given a directory of images (with a certain expected structure as explained below), the application will classify all the images and return the image labels.

The application consists of four components:
- `Client`: Reads the images from the given directory and sends them to the `Kafka broker(s)`.
- `Server`: A simple http server that (1) receives images from the `Client` and sends them to the `Kafka broker(s)`, (2) consumes the class names for the images and writes them to the database. (Database write will be emulated with printing to console for now)
- `Kafka broker(s)`: Stores the images in a log data structure.
- `Classifier`: Consumes images from the `Kafka broker(s)`, predicts the class name for each and writes them back to the `Kafka broker(s)`.
