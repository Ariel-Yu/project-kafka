import json
from datetime import datetime
from time import sleep

import click
import confluent_kafka


@click.group()
def cli():
    """
    All funcs decorated with `@cli.command()` will be a part of the `cli` group.
    """
    pass


class Config():
    def __init__(self):
        bootstrap_servers = 'confluent-kafka:9092'
        self.topic = 'confluent-kafka-topic'
        self.producer_conf = {
            'bootstrap.servers': bootstrap_servers,
            'broker.version.fallback': '0.9.0.0',
            'api.version.request': False,
            "default.topic.config": {
                "acks": 1
            }
        }
        self.consumer_conf = {
            'bootstrap.servers': bootstrap_servers,
            'broker.version.fallback': '0.9.0.0',
            'api.version.request': False,
            'group.id': None,
            'max.poll.interval.ms': 6000,
            'session.timeout.ms': 6000,
            'default.topic.config': {
                'auto.offset.reset': 'earliest'
            }
        }


@cli.command()
def produce():
    config = Config()
    producer = confluent_kafka.Producer(config.producer_conf)

    click.echo("# Start to produce message")
    msg = str(datetime.now())
    click.echo(f"# Produce message {msg}")
    producer.produce(config.topic, value=msg)
    producer.poll(1)


@cli.command()
def consume_consumer_group_1():
    _consume('consumer_group_1')


@cli.command()
def consume_consumer_group_2():
    _consume('consumer_group_2')


def _consume(consumer_group: str):
    config = Config()
    consume_conf = config.consumer_conf
    consume_conf["group.id"] = consumer_group
    consumer = confluent_kafka.Consumer(consume_conf)
    consumer.subscribe([config.topic])

    click.echo(f"# Start to consume message from {consumer_group}")
    while True:
        msg = consumer.poll(1)
        if not msg:
            click.echo("# No message to consume")
            sleep(2)
            continue

        msg_object = {
            "value": msg.value(),
            "partition": msg.partition(),
            "topic": msg.topic(),
            "key": msg.key(),
            "offset": msg.offset()
        }
        click.echo(str(msg_object))
        click.echo(msg_object.__dir__())


if __name__ == "__main__":
    cli()
