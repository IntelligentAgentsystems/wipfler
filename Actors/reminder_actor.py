import time

from pykka import ThreadingActor, ActorRef

from Messages import ReminderMessage


class ReminderActor(ThreadingActor):
    def __init__(self, parent: ActorRef, invterval_seconds: float = 1):
        self.parent = parent
        self.interval_seconds = invterval_seconds
        super().__init__()

    def _actor_loop(self):
        super()._actor_loop()
        time.sleep(self.interval_seconds)
        self.parent.tell(ReminderMessage())