import graph_bench
import graph_store as gs
import rdflib as r

# Define some graph
gs_postgres = gs.GraphStore(open_args=["postgresql+psycopg2://localhost/newtest_sqapg", True],
                            store='SQLAlchemy')

gs_virtuoso = gs.GraphStore(open_args=[("http://localhost:8890/sparql/", "http://localhost:8890/sparql"), False],
                            store='SPARQLUpdateStore',
                            identifier=r.URIRef("http://localhost/tmp_store"))

graph_dict = {'postgres': gs_postgres, 'virtuoso': gs_virtuoso}


# Start benchmarking
gb = graph_bench.GraphBench(graph_dict, "/tmp/test.csv", time_indicator='real', n_repeat=3)


def n_inserts(n, graph):
    for i in xrange(n):
        subj = r.URIRef("http://localhost/multi_insert/subject/%s" % i)
        pred = r.RDF.type
        obj = r.URIRef("http://localhost/multi_insert/object/%s" % i)

        graph.add((subj, pred, obj))


@gb.bench
def one_insert(graph):
    n_inserts(1, graph)


@gb.bench
def k1_inserts(graph):
    n_inserts(1000, graph)


@gb.bench
def k5_inserts(graph):
    n_inserts(5000, graph)


@gb.bench
def k10_inserts(graph):
    n_inserts(10000, graph)
