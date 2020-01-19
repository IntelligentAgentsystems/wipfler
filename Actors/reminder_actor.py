import logging
import time

from pykka import ThreadingActor, ActorRef

from Messages import ReminderMessage


class ReminderActor(ThreadingActor):
    def __init__(self, parent: ActorRef, invterval_seconds: float = 1):
        self.parent = parent
        self.interval_seconds = invterval_seconds
        super().__init__()

    def on_start(self):
        time.sleep(self.interval_seconds)
        self.parent.tell(ReminderMessage())
        self.stop()

    def on_failure(self, exception_type, exception_value, traceback):
        logging.log(logging.ERROR, exception_type(exception_value))
