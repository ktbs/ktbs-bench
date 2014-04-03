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

- [f( number of triples in one graph ) = query time](../../bench_results/figure_ntriples_stores_1.pdf)
- [f( number of graphs in one store ) = query time](../../bench_results/figure_ngraph_store_1.png)


third? meeting:

- cf feuille Analyse


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
