# -*- coding: utf-8 -*-

import csv
from functools import wraps

from utils.timer import Timer


class GraphBench:
    def __init__(self, output_file, time_indicator):
        self.results = {}  # Results row: function, column: graph
        self.list_graph = ['NoneDB']
        self.output_file = output_file
        self.time_indicator = time_indicator
        # Generate csv header
        with open(self.output_file, 'wb') as csv_file:
            csv_writer = csv.DictWriter(csv_file, ['func_name'] + self.list_graph)
            csv_writer.writeheader()

    def bench(self, func):
        """Decorator to run a benchmark on selected function"""
        timer = Timer(tick_now=False)  # don't tick now, func() is only called on run()

        # Make a timer wrapper, func() is executed only when time_wrapper() is called
        @wraps(func)
        def time_wrapper(*args, **kwargs):
            timer.start()
            func(*args, **kwargs)
            timer.stop()
            return timer.get_times()

        # Benchmark func against each graph
        row = {'func_name': func.__name__}
        for graph_name in self.list_graph:
            times = time_wrapper()
            self.results[func.__name__] = {graph_name: times}
            row[graph_name] = times[self.time_indicator]  # get real time for func

        # Write bench to csv
        with open(self.output_file, 'ab') as csv_file:
            csv_writer = csv.DictWriter(csv_file, ['func_name'] + self.list_graph)
            csv_writer.writerow(row)
