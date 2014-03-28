kTBS Bench
==========

This project aims at exploring performance bottlenecks of the [kTBS](http://liris.cnrs.fr/sbt-dev/ktbs).

It is made of:

- custom libraries for benchmarking (see also [sutils](https://github.com/vincent-octo/sutils))

- scripts to test some performance scenari

- results graph and their associated notes and explanations


How to setup this project
-------------------------
  1. Clone this repository using `git`.

  2. Make it a python virtual environment by `cd`ing to the project directory
     and `virtualenv .`.

  3. Activate the virtual environment: `source bin/activate`.

  4. Install the necessary python packages: `pip install -r requirements.txt`.


Notes
-----

### How to read them
Either in plain Mardown, by going in the directory `notes/content` and browsing the files.

Or by launching [Pelican](http://blog.getpelican.com/):

1. Make sure that you have the following python packages installed:
    - Pelican
    - Markdown
    - Fabric

2. Go in the directory `notes` and launch `fab serve`.
   You can now browse the html content on [http://localhost:8100]().

### How to make changes
Edit an existing file by following the [Markdown syntax](http://daringfireball.net/projects/markdown/syntax).

Or create new files in `notes/content` (checkout existing files for formatting).

License
-------
MIT, see [LICENSE](/LICENSE) file.
