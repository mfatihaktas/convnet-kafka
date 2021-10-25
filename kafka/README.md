# kafka

`KafkaProducer` and `KafkaConsumer` are Python classes that provide a basic API to write/read strings to/from Kafka brokers.
* `KafkaProducer` enables writing a <`key`, `value`> on a `topic`. It also allows for handling a write failure.
* `KafkaConsumer` enables subscribing to a list of `topic`'s and read <`key`, `value`>'s from each. Kafka ensures that pairs with the same `key` are read in order.

See [Inputs](#inputs) for detailed explanation on their behavior, and how to modify it if needed.

## Installation
There is no need to install, just import `KafkaProducer`/`KafkaConsumer` from `producer.py`/`consumer.py`.

## Dependencies
- [Kafka Python Client](https://docs.confluent.io/clients-confluent-kafka-python/current/overview.html)

## Usage
<a name="usage"></a>
The examples below require a kafka broker to be listening on `localhost:9093` for bootstrapping. See [examples/docker_compose.yml](examples/docker_compose.yml) and [examples/compose.sh](examples/compose.sh) on how to startup a containerized kafka environment on your local machine.


### An example usage of `KafkaProducer`
```python
from producer import KafkaProducer

def handle_failed_send(producer, topic, key, value):
  # Retry send
  producer.send(topic, key, value)

producer = KafkaProducer(producer_id='p0', bootstrap_servers='localhost:9093', handle_failed_send)
topic, key = 'test', producer_id
producer.send(topic, key, value='v1')
producer.send(topic, key, value='v2')
producer.send(topic, key, value='v3')
```
The full implementation is available at [examples/test_producer.py](examples/test_producer.py).

Producer writes to kafka with `send(topic, key, value)` in which each argument has to be a string.
By default, `send()` will return back to the producer's main thread after record is acknowledged to be written to the corresponding leader broker. As explained in [Inputs](#inputs) below, this behavior can be overwritten by setting the key `acks` in the optional argument `additional_conf` of `KafkaProducer`. Further details on `Kafka Acks` can be easily found online, e.g., [here](https://betterprogramming.pub/kafka-acks-explained-c0515b3b707e).

### An example usage of `KafkaConsumer`
```python
from consumer import KafkaConsumer

def callback_on_receive(topic: str, key: str, value: str):
  print("Received; topic= {}, key= {}, value= {}".format(topic, key, value))

consumer = KafkaConsumer(group_id='g0', bootstrap_servers='localhost:9093',
                         topic_list=['test'], msg_callback=callback_on_receive)
print("Enter to terminate")
input()
consumer.close()
```

The full implementation is available at [examples/test_consumer.py](examples/test_consumer.py).

As soon as an instance of `KafkaConsumer` is constructed, a thread is started to continuously poll the kafka brokers and consume from the topics in `topic_list`. Anytime a <`key`, `value`> pair is read from a `topic`, `msg_callback` is called with `topic`, `key` and `value` as its arguments. Continuous polling of the topics is executed in a separate thread to allow the main thread to shutdown the consumer whenever needed via `close()`.

### Inputs to `KafkaProducer`
<a name="inputs"></a>
- `producer_id`: ID of the producer. Should be a string. It is used to set `client.id` property of the kafka producer.

- `bootstrap_servers`: Comma-separated list of addresses at which the kafka brokers are listening for bootstrapping. It should be given as a string. It is used to set the `bootstrap.servers` property of the kafka producer..

- `handle_failed_send`: A callback function to handle failed send. It will be called with the `topic`, `key`, `value` that failed to be sent to the kafka broker.

- `additional_conf`: An optional dictionary input to configure the properties of the kafka producer. It can be used to set any of the properties available for producers in [Kafka Python Client](https://docs.confluent.io/clients-confluent-kafka-python/current/overview.html). As mentioned in [Usage](#usage), this argument can be used to overwrite the `acks` property to `0` or `all`. Note that even if `bootstrap.servers` and `client.id` are set in `additional_conf`, their values are set by the first two inputs: `producer_id` and `bootstrap_servers`.

### Inputs to `KafkaConsumer`
<a name="inputs"></a>
- `group_id`: ID of the group of consumers that the instantiated consumer will be part of. Should be a string. It is used to set `group.id` property of the kafka consumer.

- `bootstrap_servers`: Same as the one for `KafkaProducer`.

- `topic_list`: List of topics to subscribe.

- `msg_callback`: The callback function that is called by `KafkaConsumer` with every `topic`, `key`, `value` that is read from the kafka broker(s).

## Useful references on Kafka
- [Kafka Python Client](https://docs.confluent.io/clients-confluent-kafka-python/current/overview.html)
- [Kafka Listeners - Explained](https://rmoff.net/2018/08/02/kafka-listeners-explained/)
- [The Power of Kafka Partitions: How to Get the Most out of Your Kafka Cluster](https://www.instaclustr.com/the-power-of-kafka-partitions-how-to-get-the-most-out-of-your-kafka-cluster/)
- [Bitnami Docker Image for Kafka](https://github.com/bitnami/bitnami-docker-kafka)
- [kcat (formerly kafkacat) Utility](https://docs.confluent.io/platform/current/app-development/kafkacat-usage.html)
