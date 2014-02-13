# -*- coding: utf-8 -*-

"""
Utilities for the benchmarking platform.
"""

import resource
from operator import sub
from time import time


### BENCHMARKING UTILITIES
def timeit():
    """Returns process times and wall clock time."""
    usr, sys = clock2()
    return usr, sys, usr+sys, time()


def clock2():
    """Get process usr and sys time.

    This is the preferred way of getting a process timing.
    One could use time.clock(), but it happens to have wraparound problems.
    """
    return resource.getrusage(resource.RUSAGE_SELF)[:2]


def add_delta_time(sum_list, tstart, tend):
    """Add a list of delta times to a global list."""
    delta = map(sub, tend, tstart)
    for ind, item in enumerate(delta):
        sum_list[ind] += item


### MISCELLANEOUS UTILITIES

def list_sub(a, b):
    """Substract two lists item-wise.

    Performs a - b.
    """
    return map(sub, a, b)
