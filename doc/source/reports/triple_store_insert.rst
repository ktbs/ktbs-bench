.. Benchmarking triple-store insert capabilities
   Created: 2014-03-28

Benchmarking insert into triple stores
======================================

The kTBS structure
------------------

The kTBS hierarchy is as follows:

-  a RESTful API speaks over HTTP to:
-  the kTBS itself, it uses:
-  `rdflib <https://rdflib.readthedocs.org/en/latest/>`__ for managing
   the RDF parts, which in turn uses:
-  stores, such as Sleepycat,
   `Virtuoso <http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/>`__,
   PostgreSQL (over
   `rdflib-sqlalchemy <https://github.com/RDFLib/rdflib-sqlalchemy>`__)
   and much more, for storing data.

Our first concern was about the rdflib and store stages. So we let alone
the kTBS and its HTTP layer in the first place.

In search of a good bench
-------------------------

Before implementing anything, we searched for existing benchmarks on
triple-stores and anything SPARQL related.

We found some interesting work:

-  `SP2Bench <http://dbis.informatik.uni-freiburg.de/forschung/projekte/SP2B/>`__
   can make consistent set of an arbitrary number of triples, defines
   some queries to test different scenari.
-  `BSBM <http://wifo5-03.informatik.uni-mannheim.de/bizer/berlinsparqlbenchmark/>`__:
   benchmarks in a e-commerce scenario.
-  `DBPSB <http://aksw.org/Projects/DBPSB.html>`__: SPARQL benchmark
   using `DBpedia <http://dbpedia.org/About>`__.
-  `LUBM <http://aksw.org/Projects/DBPSB.html>`__: inference and
   reasoning capabilities of RDF engines.

We settled for SP2Bench because we can use it to make graphs of
different sizes and it already defines interesting queries to benchmark
the store that handles the graphs.

Benchmarking triples insertion
------------------------------

The first task we did was to benchmark different stores for the
insertion of triples.

What we have: stores and triples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The stores we used are:

-  Sleepycat
-  `Virtuoso <http://virtuoso.openlinksw.com/dataspace/doc/dav/wiki/Main/>`__
-  `Jena <https://jena.apache.org/>`__/Fuseki
-  `4store <http://4store.org/>`__
-  PostgreSQL (with
   `rdflib-sqlalchemy <https://github.com/RDFLib/rdflib-sqlalchemy>`__
   and
   `rdflib-postgresql <https://github.com/RDFLib/rdflib-postgresql>`__)
-  SQLite (with
   `rdflib-sqlalchemy <https://github.com/RDFLib/rdflib-sqlalchemy>`__
   and `rdflib-sqlite <https://github.com/RDFLib/rdflib-sqlite>`__)
-  MySQL

We used a set of approximetly 32 000 triples.

What we found
~~~~~~~~~~~~~

This was the first experiment I did with RDFLib and various stores.
Therefore, it is prone to inaccuracy and I think that the tests should
be re-run for accurate time measures.

However, this experiment raised some interesting points and bugs.

Time measurement
^^^^^^^^^^^^^^^^

There are different time measures: *usr*, *sys*, *wall* (also called
*real*).

We ended up choosing *real* because our goal is to know how much time a
user will wait. *usr* and *sys* times don't seem to account for work
doing by the triple-store but only by the time spent in Python.

Bulk inserts are better than iterative inserts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a store supports it, use bulk insertion with ``graph.addN()``. It is
much faster. Another way of using ``graph.addN()`` is to parse a file in
memory in tempory graph ``mem``, then load this graph into the one you
want: ``graph += mem``. It will use ``addN()``.

Bug in `rdflib-sqlachemy <https://github.com/RDFLib/rdflib-sqlalchemy>`__: ``addN()`` don't write anything
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Reported here: https://github.com/RDFLib/rdflib-sqlalchemy/pull/8

Slow bulk insertion with `rdflib-sqlachemy <https://github.com/RDFLib/rdflib-sqlalchemy>`__
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is no real bulk insertion with rdflib-sqlachemy, as it commits for each triple. Reported here:
https://github.com/RDFLib/rdflib-sqlalchemy/issues/9 and https://github.com/RDFLib/rdflib/issues/357

Cannot insert blank nodes in sparqlstores
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fix provided by `@pchampin <https://github.com/pchampin>`__ as an
alternative SPARQLStore: ``bnsparqlstore.py``. It converts blank nodes
to special URIs.

Insert time rises with respect to store size?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Only a suspicion for Sleepycat, needs real testing.
