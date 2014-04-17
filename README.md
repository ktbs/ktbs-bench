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


How to setup this project
-------------------------

  1. Clone this repository using `git`.

  2. Make it a python virtual environment by `cd`ing to the project directory
     and `virtualenv .`.

  3. Activate the virtual environment: `source bin/activate`.

  4. Install the necessary python packages: `pip install -r requirements.txt`.

     If you want to run the examples, you have to install `pandas`, `matplotlib` and `numpy`.
     These libraries have been excluded by default because they are heavy.
     Either uncomment the corresponding lines in [`requirements.txt`](requirements.txt) or use
     your package manager to install them.


Running benchmarks
------------------

You can run the benchmark example like so: `python bench_examples/bench_queries.py`.

You can also define your own benchmarks. See `bench_examples/bench_queries.py` for a template.
You might want to read the [documentation of `ktbs_bench_manager`] [kbm-doc].

Furthermore, you can run a batch of benchmarks by using the [`bench.py`](bin/bench.py) script.
Use `bin/bench.py --help` for more information.


Reading and writing notes
-------------------------

### How to read them
The easiest solution is to read the plain Markdown notes,
by going in the directory `notes/content` and browsing the files.

The not-as-easy solution is to read them through [Pelican] [pelican-web] :

1. Make sure that you have the following python packages installed:
    - Pelican
    - Markdown
    - Fabric

   You can use `pip install Pelican fabric Markdown` to install them.

2. Go in the directory `notes` and launch `fab serve`.
   You can now browse the html content on [http://localhost:8100]().

### How to make changes
Edit an existing file by following the [Markdown syntax](http://daringfireball.net/projects/markdown/syntax).

Or create new files in `notes/content` (checkout existing files for formatting).


License
-------
MIT, see [LICENSE](/LICENSE) file.


[pelican-web]: http://blog.getpelican.com/
[report-query]: notes/content/report_triple-store-query.md
[report-insert]: notes/content/report_triple-store-insert.md
[kbm-doc]: https://github.com/vincent-octo/ktbs_bench_manager/blob/master/ktbs_bench_manager/bench_manager.py
