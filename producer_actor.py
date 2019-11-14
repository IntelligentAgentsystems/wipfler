import pykka
import random
import threading
from time import sleep


class ProducerActor(pykka.ThreadingActor):

    def __init__(self, consumer):
        super().__init__()
        self.consumer = consumer
        self._is_up = False

    def send_randomly(self):
        while self._is_up:
            if random.randrange(0, 5) == 0:
                self.consumer.tell(f'Message{random.randrange(1000, 10000)}')
            else:
                sleep(0.5)

    def on_start(self):
        self._is_up = True
        threading.Thread(target=self.send_randomly())

    def stop(self):
        self._is_up = False

