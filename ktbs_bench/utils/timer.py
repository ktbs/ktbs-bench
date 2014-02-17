import resource
from time import clock


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
        times.append(clock())
        return times

    def stop(self):
        """Stop the timer and compute delta time."""
        self.stop_time = self.tick()
        self.delta = [stop - start for start, stop in zip(self.start_time, self.stop_time)]

    def __repr__(self):
        return 'usr: %s\tsys: %s\tusr+sys: %s\t real: %s' %\
               (self.delta[0], self.delta[1], self.delta[0]+self.delta[1], self.delta[2])
