from contextlib import contextmanager
from csv import DictWriter
import logging

from ktbs_bench.utils.decorators import bench as util_bench


class BenchManager:
    def __init__(self):
        self._contexts = []
        self._bench_funcs = []
        self._results = {}

    def bench(self, func):
        """Prepare a function to be benched and add it to the list to be run later."""
        func = util_bench(func)
        self._bench_funcs.append(func)

    def context(self, func):
        """Decorate a function to act as a context."""
        func = contextmanager(func)
        self._contexts.append(func)

    def run(self, output_filename, show_log=False):
        """Execute each collected function against each context."""
        # Run the bench for each function against each context
        if show_log:
            logging.getLogger().setLevel(logging.INFO)
        for func in self._bench_funcs:
            self._results[func.__name__] = {}
            if show_log:
                logging.info('Func: %s' % func.__name__)
            for context in self._contexts:
                if show_log:
                    logging.info('with context: %s' % context.__name__)
                with context() as arg:
                    if not isinstance(arg, tuple):
                        arg = tuple([arg])  # Make arg a tuple of one element
                    _, res_time = func(*arg)
                self._results[func.__name__][context.__name__] = res_time

        # Write output to a CSV file
        fieldnames = ['func_name']
        fieldnames += [context.__name__ for context in self._contexts]
        with open(output_filename, 'wb') as output_file:
            csv_file = DictWriter(output_file, fieldnames)
            csv_file.writeheader()

            for func_name, env_results in self._results.items():
                row_results = env_results
                row_results['func_name'] = func_name
                csv_file.writerow(row_results)
