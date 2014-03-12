from contextlib import contextmanager
from csv import DictWriter
import logging

from ktbs_bench.utils.decorators import bench as util_bench


class BenchManager(object):
    """
    Manage benchmarks by timing function against different contexts.

    General concept
    ===============
    A BenchManager is instantiated in order to collect functions
    to benchmark, like so:
    >>> my_bench_manager = BenchManager()

    In order to add functions to bench, one flag them for bench
    by using the :meth:`bench` decorator. For example:
    >>> @my_bench_manager.bench
    ... def add_one(n):
    ...     return n + 1

    Each flagged function is then called against contexts.
    A context is a function with optional setup and teardown, and it
    must *yield* the parameter that benchmarked functions need.
    >>> @my_bench_manager.context
    ... def three():
    ...     # optional setup
    ...     try:
    ...        # yield the parameter
    ...        yield 3
    ...     finally:
    ...        # optional teardown
    ...        pass

    Finally, to perform the benchmarks, one must call:
    >>> my_bench_manager.run('/tmp/my_results.csv')

    The result of the two examples above is to time ``add_one(3)``.

    Technical details
    =================
    Each context is stored in the list :attr:`_contexts`.
    Each function to benchmark is stored in the list :attr:`_bench_funcs`.

    When :meth:`run` is called, it will iterate over functions and contexts
    to call each function against each context.
    """
    def __init__(self):
        self._contexts = []
        self._bench_funcs = []
        self._results = {}

    def bench(self, func):
        """Prepare a function to be benched and add it to the list to be run later.

        :param function func: the function to bench
        """
        func = util_bench(func)
        self._bench_funcs.append(func)

    def context(self, func):
        """Decorate a function to act as a context.

        :param function func: the function that describes the context
        """
        func = contextmanager(func)
        self._contexts.append(func)

    def run(self, output_filename, show_log_info=False):
        """Benchmark functions against contexts.

        :param str output_filename: filename of the CSV output
        :param bool show_log_info: True to display log during the run, False otherwise
        """
        if show_log_info:
            logging.getLogger().setLevel(logging.INFO)

        # Run the bench for each function against each context
        for func in self._bench_funcs:
            self._results[func.__name__] = {}
            for context in self._contexts:
                with context() as arg:  # catch what the context yield
                    if not isinstance(arg, tuple):
                        arg = tuple([arg])  # make arg a tuple of one element
                    _, res_time = func(*arg)  # call func with what the context yielded
                logging.info('Benchmarking function %s with context %s: %s s' %
                             (func.__name__, context.__name__, res_time))
                self._results[func.__name__][context.__name__] = res_time

        # Write output to a CSV file
        self.write_output(output_filename)

    def write_output(self, output_filename):
        """Write results of the BenchManager to a nicely formatted CSV file.

        :param str output_filename: filename of the CSV output
        """
        # Get column names
        fieldnames = ['func_name']
        fieldnames += [context.__name__ for context in self._contexts]

        # Create the CSV with header and results
        with open(output_filename, 'wb') as output_file:
            csv_file = DictWriter(output_file, fieldnames)
            csv_file.writeheader()

            for func_name, env_results in self._results.items():
                row_results = env_results
                row_results['func_name'] = func_name
                csv_file.writerow(row_results)
