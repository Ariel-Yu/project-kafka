from datetime import datetime


class MultiConsumerGroupsProduceService:
    def __init__(self, producer):
        self.producer = producer

    def produce(self, topic: str):
        msg = str(datetime.now())
        print(f"##### Produce message: {msg}")
        self.producer.produce(topic, value=msg)