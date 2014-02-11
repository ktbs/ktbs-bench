# -*- coding: utf-8 -*-

"""
Benchmarking utilities.

"""

import resource
from operator import sub, add


def clock2():
    """Get process usr and sys time.

    This is the preferred way of getting a process timing.
    One could use time.clock(), but it happens to have wraparound problems.
    """
    return resource.getrusage(resource.RUSAGE_SELF)[:2]


def add_delta_time(sum, tstart, tend):
    """Add a list of delta times to a global list."""
    delta = map(sub, tend, tstart)
    for ind, item in enumerate(delta):
        sum[ind] += item
