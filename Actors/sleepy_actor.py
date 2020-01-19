import time

from pykka import ThreadingActor


class SleepyActor(ThreadingActor):

    def __init__(self, time_to_sleep: float):
        super().__init__()
        self.time_to_sleep = time_to_sleep

    def on_start(self):
        super().on_start()
        time.sleep(self.time_to_sleep)
        return
