import resource
import logging
from time import time


class Timer:
    """Measure process duration."""
    def __init__(self, tick_now=True):
        self.start_time = []
        if tick_now:
            self.start_time = self.tick()
        self.stop_time = None
        self.delta = None

    @staticmethod
    def tick():
        """Return usr, sys and real times."""
        times = list(resource.getrusage(resource.RUSAGE_SELF)[:2])
        times.append(time())
        return times

    def start(self):
        """Start the timer"""
        if self.start_time != []:
            logging.warning('Start time has already been set. Continuing with previous value.')
        else:
            self.start_time = self.tick()

    def stop(self):
        """Stop the timer and compute delta time."""
        self.stop_time = self.tick()
        self.delta = [stop - start for start, stop in zip(self.start_time, self.stop_time)]

    def __repr__(self):
        if self.stop_time is not None:
            res = 'usr: %s\tsys: %s\tusr+sys: %s\t real: %s' %\
                  (self.delta[0], self.delta[1], self.delta[0]+self.delta[1], self.delta[2])
        else:
            res = 'timer has not been stopped.'
        return res
