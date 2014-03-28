Title: Benchmarking triple-store query capabilities
Date: 2014-03-28
Category: report
Tags: info, triple-store, benchmark
Author: Vincent

TODO: get info from: mail, figures

data: SP2B

first meeting:

- my own tests
- next--> another perspective on time (one graph per store)
- (get figure, maybe from raw data or from email)

sncd meeting:

- discarding some triple stores (cf other article)
- the other perspectives:
    - f( number of triples in one graph ) = query time
    - f( number of graphs in one store ) = query time


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
