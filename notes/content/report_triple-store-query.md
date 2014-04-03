Title: Benchmarking triple-store query capabilities
Date: 2014-03-28
Category: report
Tags: info, triple-store, benchmark
Author: Vincent



Context
=======

After some experiments with [triple insertion](report_triple-store-insert.md), we decided to refocus
on store queries because it is a widely used scenario for kTBS users.

The goal is to explore the capabilities of several triple stores for different query types.

The queries we used are taken from [SP2Bench][sp2bench-queries].


Results
=======

Exploration
-----------

We first explored the different stores against the queries.
Each store had one graph of 500 triples.
Queries ran anywhere from 5 ms to 5000 s depending on the store and the query.
Results here: [query32000_full.ods](../../bench_results/query32000_full.ods).

It's a bar plot: each bar is query for a store (resulting in nb queries * nb store bars).
The y-axis is the query time (real time).
Tested stores are:

- Virtuoso
- 4store
- PostgreSQL
- Sleepycat
- In-memory
- Jena/Fuseki

Results also showed variation between runs.
We decided to make more runs to have a good idea of the mean and look at the standard variation to see
if the results were ok.


Changing perspective
--------------------

We changed how we looked at results. We wanted to see the evolution of query times against the number of
triples in one graph, or the number of graphs per store.

We also discarded some triple stores, see [report_bench-selected-stores.md]().

Results:

- [f( number of graphs in one store ) = query time](../../bench_results/figure_ngraph_store_1.png)
- [f( number of triples in one graph ) = query time](../../bench_results/figure_ntriples_stores_1.pdf)


### Comments on f( number of graphs in one store ) = query time

We observe that all measures for 5 graph / store are greater than the other ones.
This lead us to dismiss these points.

For *4store* there are only measures for 1 graph / store.
When trying to insert triples for 5 graphs / store in 4store, the computer started to swap and never finished.
A decision was made to stop testing this store.

For *Sleepycat*, *Postgres* and *Virtuoso*, most of the query times seem to be constant with respect to
the number of graph per store. Except for a few queries like q2 and q12a for Sleepycat and Postgres, and q2, q3b, q3c and q9 for Virtuoso.

We observe a weird behavior of *Sleepycat* and *PostgreSQL* on query 12a.
This query is the same query as q5a, except q12a is a `ASK` and q5a is a `SELECT`.
It turns out that q12a takes longer than q5a.
This only appears on stores directly managed by RDFlib, which lead us to think that it's a bug in how RDFlib
handles some `ASK` queries.

q2 acces large strings (abstract of articles), which is a reason why it takes longer than the other queries.


### Comments on f( number of triples in one graph ) = query time

We tested the query times as function of the number of triples in one graph in the stores: Sleepycat, PostgreSQL and Virtuoso.

The measures were:

- 32000 triples
- 256000 triples
- 1000000 triples

For PostgreSQL, queries 2 and 12a were not done for 1m triples, as it would have taken too much time.

For Sleepycat, all queries were not done for 1m triples. I was unable to insert 1m triples in a Sleepycat store, running the insert for 1 day was not sufficient. Plus, the python process was at state *sleeping*.
Another try at this should be done.

Queries for PostgreSQL are constant in times (except q2 and 12a).
It seemes to be the same thing for Sleepycat, but we don't have points for 1m triples.
Both PostgreSQL and Sleepycat queries (except q2 and q12a) are in the range 10-100 ms, which is accetable.

Allmost all Virtuoso queries are in the range 10-5000 ms. There are greater variation between queries than with PostgreSQL and Sleepycat.
Further more, we don't have a clear understanding of a how the queries behave.
We see that most queries takes more time when runing on a 256k triples graph than on a 32k triples graph.
But most queries takes approximetly the same time, or even less time, when performing on 1m triples than on 256k triples graph.

This tests should be run another time for more accurate and understanble results.
Additionnal points should be measured (64k, 128k, 512k, 700k triples / store).


Discarding queries
------------------
fourth:

- cleanup some queries that took too much time


fifth?:

- forks (first time, open close outside of fork --> sleepycat error, cf other article)
- goal: simulate multiple user using kTBS at the same time


sixth:

- forks w/ open-close inside each fork --> we are measuring the time taken by open/close and the time taken
by the queries as open/close is ~ 1s and a query is ~ 0.01s.


seventh:

- forks w/ open-close and query cocktail



[sp2bench-queries]: http://dbis.informatik.uni-freiburg.de/index.php?project=SP2B/queries.php
