Title: Benchmarking triple-store insert capabilities
Date: 2014-03-28
Category: report
Tags: info, triple-store, benchmark
Author: Vincent

data: SP2B, bench_results/res_iter-insert.md    
triple-stores: postgres, postgres-sqlalchemy, sqlite, sqlite-sqlalchemy, virtuoso, jena, 4store

time measurement: different times : usr, sys, usr+sys, wall/real
we end up choosing real because our goal is to know how much time a user will wait, beside usr and sys times don't seem
to account for work doing by the triple-store.

discover rdflib-sqlalchemy bug addN() would not insert anything in the database : https://github.com/RDFLib/rdflib-sqlalchemy/pull/8

very slow bulk insertion with rdflib-sqlalchemy: https://github.com/RDFLib/rdflib-sqlalchemy/issues/9
and https://github.com/RDFLib/rdflib/issues/357

