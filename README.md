kTBS Bench
==========

This project aims at exploring performance bottlenecks of the [kTBS](http://liris.cnrs.fr/sbt-dev/ktbs).

It is made of:

- custom libraries for benchmarking (see also [sutils](https://github.com/vincent-octo/sutils))

- scripts to test some performance scenari

- results graph and their associated notes and explanations


Results
-------

Reports on our findings are :

- [Report on query benchmarks] [report-query]

- [Report on insert benchmarks] [report-insert]

More information is available via the [online documentation](http://ktbs-bench.readthedocs.org/en/latest/index.html).


How to setup this project
-------------------------

  1. Clone this repository using `git`.

  2. Make it a python virtual environment by `cd`ing to the project directory
     and `virtualenv .`.

  3. Activate the virtual environment: `source bin/activate`.

  4. Install the necessary python packages: `pip install -r requirements.txt`.

     If you don't want to run the examples, you should uncomment the lines corresponding to
     the heavy libraries `pandas`, `matplotlib` and `numpy` in [`requirements.txt`](requirements.txt).


Running benchmarks
------------------

You can run the benchmark example like so: `python bench_examples/bench_queries.py`.

You can also define your own benchmarks. See `bench_examples/bench_queries.py` for a template.
You might want to read the [documentation of `ktbs_bench_manager`] [kbm-doc].

Furthermore, you can run a batch of benchmarks by using the [`bench.py`](bin/bench.py) script.
Use `bin/bench.py --help` for more information.


Documentation
-------------
The [documentation for this project][kb-doc] is available on readthedocs.
The reports on our findings are there too.


License
-------
MIT, see [LICENSE](/LICENSE) file.


[pelican-web]: http://blog.getpelican.com/
[report-query]: https://ktbs-bench.readthedocs.org/en/latest/reports/triple_store_query.html
[report-insert]: https://ktbs-bench.readthedocs.org/en/latest/reports/triple_store_insert.html
[kb-doc]: http://ktbs-bench.readthedocs.org/en/latest/
[kbm-doc]: https://ktbs-bench-manager.readthedocs.org/en/latest/bench_manager.html
