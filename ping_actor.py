import pykka
import urns
import time


class PingActor(pykka.ThreadingActor):

    def __init__(self):
        super().__init__()

    def on_start(self):
        super().on_start()
        self.actor_urn = urns.PONG_URN
        print(f'Started {self.__class__.__name__}')

    def on_receive(self, message):
        print(f'Recieved {message}')
        time.sleep(.1)
        pong_actor = pykka.ActorRegistry.get_by_class_name('PongActor')[0]
        pong_actor.tell('PING')

    def on_stop(self):
        print(f'Stopped {self.__class__.__name__}')
        super().on_stop()

