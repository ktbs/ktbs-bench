# -*- coding: utf-8 -*-

from functools import wraps

from utils.timer import Timer


class GraphBench:
    def __init__(self):
        self.results = {}  # Results row: function, column: graph
        self.list_graph = []

    def bench(self, func):
        timer = Timer(
            tick_now=False)  # don't tick now as this is called on file parsing, func() is only called on run()

        @wraps(func)
        def wrapper(*args, **kwargs):
            timer.start()
            func(*args, **kwargs)
            timer.stop()
            return timer.get_times()

        self.results[func] = {}
        return wrapper

    def run(self):
        """Run all the benchmarks"""
        for func in self.results.keys():
            self.results[func] = func()  # TODO ne fonctionne pas comme prévu…
