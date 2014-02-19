import resource
import logging
from time import time


class Timer:
    """Measure process duration."""
    def __init__(self, tick_now=True):
        self.start_time = []
        if tick_now:
            self.start_time = self.tick()
        self.stop_time = {}
        self.delta = {}

    @staticmethod
    def tick():
        """Return usr, sys and real times."""
        usage_times = resource.getrusage(resource.RUSAGE_SELF)[:2]
        times = {'usr': usage_times[0], 'sys': usage_times[1], 'real': time()}
        return times

    def start(self):
        """Start the timer"""
        if self.start_time:
            logging.warning('Start time has already been set. Continuing with previous value.')
        else:
            self.start_time = self.tick()

    def stop(self):
        """Stop the timer and compute delta time."""
        self.stop_time = self.tick()
        for type in self.start_time.keys():
            self.delta[type] = self.stop_time[type] - self.start_time[type]

    def get_times(self):
        """Return a dict of delta times."""
        if self.delta:
            return self.delta
        else:
            logging.error("The timer has not been stopped yet.")

    def __repr__(self):
        if self.stop_time:
            res = 'usr: %s\tsys: %s\tusr+sys: %s\t real: %s' % \
                  (self.delta['usr'], self.delta['sys'], self.delta['usr'] + self.delta['sys'], self.delta['real'])
        else:
            res = 'timer has not been stopped.'
        return res
