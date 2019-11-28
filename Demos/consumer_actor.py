import pykka

class ConsumerActor(pykka.ThreadingActor):

    def __init__(self):
        super().__init__()

    def on_receive(self, message):
        print(message)