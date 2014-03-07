import resource
import logging
from time import time


class Timer(object):
    """
    Measure process duration.

    The timer is a little object that must be started and stopped to compute
    delta times.

    Examples
    --------
    Measuring time
    >>> from time import sleep
    >>> my_timer = Timer()  # timer start at instantiation by default
    >>> sleep(1)
    >>> my_timer.stop()
    >>> # Get the delta times
    >>> times = my_timer.get_times()
    >>> 1 < times['real'] < 1.1
    True
    """

    def __init__(self, tick_now=True):
        self.start_time = []
        if tick_now:
            self.start_time = self.tick()
        self.stop_time = {}
        self.delta = {}

    @staticmethod
    def tick():
        """Return real, sys and usr times.

        Returns
        -------
        usr : float
            User CPU time since the start of the process.
        sys : float
            System CPU time since the start of the process.
        real : float
            Time since the start of the UNIX epoch.

        References
        ----------
        .. [1] Ipython %time magic command implementation http://git.io/GJpSNA
        """
        usage_times = resource.getrusage(resource.RUSAGE_SELF)[:2]
        times = {'usr': usage_times[0], 'sys': usage_times[1], 'real': time()}
        return times

    def start(self):
        """Start the timer."""
        if self.start_time:
            logging.warning('Start time has already been set. Continuing with previous value.')
        else:
            self.start_time = self.tick()

    def stop(self):
        """Stop the timer and compute delta time."""
        self.stop_time = self.tick()
        for time_type in self.start_time.keys():
            self.delta[time_type] = self.stop_time[time_type] - self.start_time[time_type]

    def get_times(self):
        """Return a dict of delta times."""
        if self.delta:
            return self.delta
        else:
            logging.error("The timer has not been stopped yet.")

    def __repr__(self):
        """String representation of Timer delta times."""
        if self.stop_time:
            res = 'usr: %s\tsys: %s\tusr+sys: %s\t real: %s' % \
                  (self.delta['usr'], self.delta['sys'], self.delta['usr'] + self.delta['sys'], self.delta['real'])
        else:
            res = 'timer has not been stopped.'
        return res
