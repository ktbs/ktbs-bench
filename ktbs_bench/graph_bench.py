# -*- coding: utf-8 -*-

import csv
from functools import wraps

from utils.timer import Timer


class GraphBench:
    def __init__(self, graph_dict, output_file, time_indicator, n_repeat=1, csv_header=True):
        self.results = {}  # Results row: function, column: graph
        self.graph_dict = graph_dict
        self.output_file = output_file
        self.time_indicator = time_indicator
        self.n_repeat = n_repeat
        # Generate csv header
        if csv_header:
            with open(self.output_file, 'wb') as csv_file:
                csv_writer = csv.DictWriter(csv_file, ['func_name'] + self.graph_dict.keys())
                csv_writer.writeheader()

    def bench(self, func):
        """Decorator to run a benchmark on selected function"""
        # Make a time wrapper, func() is executed only when time_wrapper() is called
        @wraps(func)
        def time_wrapper(timer, graph):
            graph.connect()
            timer.start()
            func(graph)
            timer.stop()
            graph.close()
            return timer.get_times()

        # Benchmark func against each graph
        row = {'func_name': func.__name__}
        for graph_name in self.graph_dict.keys():
            times = []
            for _ in xrange(self.n_repeat):
                times.append(time_wrapper(Timer(tick_now=False), self.graph_dict[graph_name]))

            # Compute mean times
            mean_times = {}
            for time in times[0].keys():
                mean_times[time] = 0
                for measure in times:
                    mean_times[time] += measure[time]
                mean_times[time] /= len(times)

            self.results[func.__name__] = {graph_name: mean_times}
            row[graph_name] = mean_times[self.time_indicator]  # get real time for func

        # Write bench to csv
        with open(self.output_file, 'ab') as csv_file:
            csv_writer = csv.DictWriter(csv_file, ['func_name'] + self.graph_dict.keys())
            csv_writer.writerow(row)
