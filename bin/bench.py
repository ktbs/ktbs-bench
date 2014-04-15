#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Run benchmarks.

Usage:
  bench.py <bench_folder> [<output_folder>]

Options:
  -h --help     Show this help screen.

"""
from docopt import docopt
from os import listdir, path
from sys import path as sys_path


def scan_bench_files(directory):
    """Scan a directory for existing benchmark scripts.

    :param str directory: path to the directory containing the benchmark scripts
    :returns tuple:
    """
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
    arg_bench_folder = args['<bench_folder>']

    for bench_file in scan_bench_files(arg_bench_folder):
        sys_path.append(path.dirname(bench_file))  # Add script directory to sys.path in case of imports
        execfile(bench_file)
