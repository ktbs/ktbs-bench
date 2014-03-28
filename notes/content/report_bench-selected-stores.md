Title: Discarding store in the benchmarks
Date: 2014-02-26
Category: report
Tags: info, triple-store, benchmark
Author: Vincent

# Discarding Jena
When doing the benchmark on each store with 1 graph of 32000 triples, Jena proved to be very inefficient.

For query 4, it took around 1000 s. Some other queries took around 100 s.
The total time taken by Jena in the benchmark is too high if we want to make more tests with repetitions.

# Discarding 4store
When doing the benchmark on each store with 5 graph of 32000 triples per store, 4store began to swap on
query 2.

The test was stopped when swap exceeded 3 Go.

# Discarding IOMemory
IOMemory is not tested for store with more than one graph because it can't handle more than one graph.

# Discarding query 12b
After discarding Jena and 4store, the last biggest query time was with Postgres on query 12b.
So this query was discarded for all store.
