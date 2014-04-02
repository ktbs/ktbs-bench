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



data: bench_results/res_iter-insert.md
triple-stores: postgres, postgres-sqlalchemy, sqlite, sqlite-sqlalchemy, virtuoso, jena, 4store

time measurement: different times : usr, sys, usr+sys, wall/real
we end up choosing real because our goal is to know how much time a user will wait, beside usr and sys times don't seem
to account for work doing by the triple-store.

discover rdflib-sqlalchemy bug addN() would not insert anything in the database : https://github.com/RDFLib/rdflib-sqlalchemy/pull/8

very slow bulk insertion with rdflib-sqlalchemy: https://github.com/RDFLib/rdflib-sqlalchemy/issues/9
and https://github.com/RDFLib/rdflib/issues/357

future: insert time rises with store size ? (sleepycat)



[rdflib-docs]: https://rdflib.readthedocs.org/en/latest/
[rdflib-sqlalchemy-github]: https://github.com/RDFLib/rdflib-sqlalchemy
[virtuoso-home]: http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/

[sp2bench]: http://dbis.informatik.uni-freiburg.de/forschung/projekte/SP2B/
[bsbm]: http://wifo5-03.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/
[dbpsb]: http://aksw.org/Projects/DBPSB.html
[lubm]: http://aksw.org/Projects/DBPSB.html

[dbpedia]: http://dbpedia.org/About
