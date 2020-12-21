from time import sleep

import click
import confluent_kafka

from project_kafka.domain.services.multi_consumer_groups_produce_service import MultiConsumerGroupsProduceService
from project_kafka.infrastructure.factories.avro_producer_factory import AvroProducerFactory


@click.group()
def cli():
    """
    All funcs decorated with `@cli.command()` will be a part of the `cli` group.
    """
    pass


class Config:
    def __init__(self):
        bootstrap_servers = "kafka:29092"
        self.topic = 'confluent-kafka-topic'
        self.producer_conf = {
            'bootstrap.servers': bootstrap_servers,
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
    producer = AvroProducerFactory()
    service = MultiConsumerGroupsProduceService(producer)

    click.echo("##### Start to produce message")
    service.produce("topic-multi-consumer-groups")


@cli.command()
@click.argument('consumer_group_name')
def consume(consumer_group_name: str):
    config = Config()
    consumer_conf = config.consumer_conf
    consumer_conf["group.id"] = consumer_group_name
    consumer = confluent_kafka.Consumer(consumer_conf)
    consumer.subscribe([config.topic])

    click.echo(f"##### Start to consume message from {consumer_group_name}")
    while True:
        msg = consumer.poll(1)
        if not msg:
            click.echo("##### No message to consume")
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
        # click.echo(msg_object.__dir__())


if __name__ == "__main__":
    cli()