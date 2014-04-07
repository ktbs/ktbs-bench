Title: Benchmarking triple-store insert capabilities
Date: 2014-03-28
Category: report
Tags: info, triple-store, benchmark
Author: Vincent


The kTBS structure
==================

The kTBS hierarchy is as follows:

- a RESTful API speaks over HTTP to:
- the kTBS itself, it uses:
- [rdflib][rdflib-docs] for managing the RDF parts, which in turn uses:
- stores, such as Sleepycat, [Virtuoso][virtuoso-home],
  PostgreSQL (over [rdflib-sqlalchemy][rdflib-sqlalchemy-github]) and much more, for storing data.

Our first concern was about the rdflib and store stages.
So we let alone the kTBS and its HTTP layer in the first place.


In search of a good bench
=========================

Before implementing anything, we searched for existing benchmarks on triple-stores and anything SPARQL related.

We found some interesting work:

- [SP2Bench][sp2bench] can make consistent set of an arbitrary number of triples,
  defines some queries to test different scenari.
- [BSBM][bsbm]: benchmarks in a e-commerce scenario.
- [DBPSB][dbpsb]: SPARQL benchmark using [DBpedia][dbpedia].
- [LUBM][lubm]: inference and reasoning capabilities of RDF engines.

We settled for SP2Bench because we can use it to make graphs of different sizes and it already defines interesting
queries to benchmark the store that handles the graphs.


Benchmarking triples insertion
==============================

The first task we did was to benchmark different stores for the insertion of triples.


What we have: stores and triples
--------------------------------

The stores we used are:

- Sleepycat
- [Virtuoso][virtuoso-home]
- [Jena][jena-home]/Fuseki
- [4store][4store-home]
- PostgreSQL (with [rdflib-sqlalchemy][rdflib-sqlalchemy-github] and [rdflib-postgresql][rdflib-postgresql-github])
- SQLite (with [rdflib-sqlalchemy][rdflib-sqlalchemy-github] and [rdflib-sqlite][rdflib-sqlite-github])
- MySQL

We used a set of approximetly 32 000 triples.


What we found
-------------

This was the first experiment I did with RDFLib and various stores.
Therefore, it is prone to inaccuracy and I think that the tests should be re-run for accurate time measures.

However, this experiment raised some interesting points and bugs.


### Time measurement

There are different time measures: *usr*, *sys*, *wall* (also called *real*).

We ended up choosing *real* because our goal is to know how much time a user will wait.
*usr* and *sys* times don't seem to account for work doing by the triple-store but only by the time spent in Python.


### Bulk inserts are better than iterative inserts

If a store supports it, use bulk insertion with `graph.addN()`. It is much faster.
Another way of using `graph.addN()` is to parse a file in memory in tempory graph `mem`,
then load this graph into the one you want: `graph += mem`. It will use `addN()`.


### Bug in [rdflib-sqlachemy][rdflib-sqlalchemy-github]: `addN()` don't write anything

Reported here: [https://github.com/RDFLib/rdflib-sqlalchemy/pull/8]()


### Slow bulk insertion with [rdflib-sqlachemy][rdflib-sqlalchemy-github]

There is no real bulk insertion with rdflib-sqlachemy, as it commits for each triple.
Reported here: [https://github.com/RDFLib/rdflib-sqlalchemy/issues/9]()
and [https://github.com/RDFLib/rdflib/issues/357]()


### Cannot insert blank nodes in sparqlstores

Fix provided by [@pchampin](https://github.com/pchampin) as an alternative SPARQLStore: `bnsparqlstore.py`.
It converts blank nodes to special URIs.


### Insert time rises with respect to store size?

Only a suspicion for Sleepycat, needs real testing.


[rdflib-docs]: https://rdflib.readthedocs.org/en/latest/
[rdflib-sqlalchemy-github]: https://github.com/RDFLib/rdflib-sqlalchemy
[rdflib-postgresql-github]: https://github.com/RDFLib/rdflib-postgresql
[rdflib-sqlite-github]: https://github.com/RDFLib/rdflib-sqlite
[virtuoso-home]: http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/
[jena-home]: https://jena.apache.org/
[4store-home]: http://4store.org/

[sp2bench]: http://dbis.informatik.uni-freiburg.de/forschung/projekte/SP2B/
[bsbm]: http://wifo5-03.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/
[dbpsb]: http://aksw.org/Projects/DBPSB.html
[lubm]: http://aksw.org/Projects/DBPSB.html

[dbpedia]: http://dbpedia.org/About
