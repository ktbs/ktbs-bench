#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Run benchmarks.

Usage:
  bench.py [<folder>]

Options:
  -h --help     Show this help screen.

"""
from docopt import docopt
from os import listdir, path


def scan_bench_files(directory):
    """Scan a directory for benchmarks"""
    if directory is None:
        directory = '.'
    ldir = listdir(directory)
    res = filter(lambda f: f.startswith('bench_') and f.endswith('.py'),
                 ldir)
    res = map(lambda f: path.join(path.abspath(directory), f),
              res)
    return res


if __name__ == '__main__':
    args = docopt(__doc__, version='bench 0.1')
    for file in scan_bench_files(args['<folder>']):
        execfile(file)
