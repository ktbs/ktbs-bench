from contextlib import contextmanager

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

    def run(self, output_file):
        """Execute each collected function against each context."""
        for func in self._bench_funcs:
            self._results[func.__name__] = {}
            for context in self._contexts:
                with context() as arg:
                    if not isinstance(arg, tuple):
                        arg = tuple([arg])  # Make arg a tuple of one element
                    _, res_time = func(*arg)
                self._results[func.__name__][context.__name__] = res_time
