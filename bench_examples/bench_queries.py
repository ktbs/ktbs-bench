import rdflib

from ktbs_bench_manager import BenchManager
import nosparqlstore
import queries


bmgr = BenchManager(set_log_info=True)


N_RUN = 10
N_TRIPLES = 1024000
MIN_TRIPLES = 1024000
MAX_TRIPLES = 1024500


rdflib.plugin.register('BN', rdflib.store.Store, 'rdflib.plugins.stores.bnsparqlstore', 'SPARQLUpdateStore')
VIRT = {'store': 'BN',
        'id_sub': 'virtuoso',
        'open': ('http://localhost:8890/sparql/', 'http://localhost:8890/sparql/')}
PG = {'store': 'SQLAlchemy',
      'id_sub': 'postgres',
      'open': 'postgresql+psycopg2://localhost/many_graph'}
SLEEPY = {'store': 'Sleepycat',
          'id_sub': 'sleepy',
          'open': 'PATH_TO_SLEEPYCAT_DB'}


@bmgr.context
def sleepycat():
    graph_id = 'http://localhost/bench/sleepy/many_triples_%s/' % N_TRIPLES
    bs_sleepycat = nosparqlstore.get_sleepycat(SLEEPY['open'], graph_id, False)
    try:
        # Checking number of triples in graph
        bs_sleepycat.connect()
        n_triples = len(bs_sleepycat.graph)
        assert MIN_TRIPLES < n_triples < MAX_TRIPLES, "found %d triples, for graph %s" % (n_triples, graph_id)
        bs_sleepycat.close()
        logger = bmgr.get_logger()
        logger.info(
            'Sleepycat graph {graph_id} checked for {min} < {n} < {max}'.format(graph_id=bs_sleepycat.graph.identifier,
                                                                                min=MIN_TRIPLES,
                                                                                n=n_triples,
                                                                                max=MAX_TRIPLES))
        bs_sleepycat.connect()
        yield bs_sleepycat.graph
    finally:
        bs_sleepycat.close()
    del bs_sleepycat


@bmgr.bench
def qall(graph):
    graph.query(queries.QUERIES['query_all'])


@bmgr.bench
def q1(graph):
    graph.query(queries.QUERIES['q1'])


@bmgr.bench
def q3a(graph):
    graph.query(queries.QUERIES['q3a'])


@bmgr.bench
def q3b(graph):
    graph.query(queries.QUERIES['q3b'])


@bmgr.bench
def q3c(graph):
    graph.query(queries.QUERIES['q3c'])


@bmgr.bench
def q4(graph):
    graph.query(queries.QUERIES['q4'])


@bmgr.bench
def q5a(graph):
    graph.query(queries.QUERIES['q5a'])


@bmgr.bench
def q5b(graph):
    graph.query(queries.QUERIES['q5b'])


@bmgr.bench
def q6(graph):
    graph.query(queries.QUERIES['q6'])


@bmgr.bench
def q7(graph):
    graph.query(queries.QUERIES['q7'])


@bmgr.bench
def q8(graph):
    graph.query(queries.QUERIES['q8'])


@bmgr.bench
def q9(graph):
    graph.query(queries.QUERIES['q9'])


@bmgr.bench
def q10(graph):
    graph.query(queries.QUERIES['q10'])


@bmgr.bench
def q11(graph):
    graph.query(queries.QUERIES['q11'])


@bmgr.bench
def q12c(graph):
    graph.query(queries.QUERIES['q12c'])


if __name__ == '__main__':
    # Run the benchs
    for ind_run in xrange(N_RUN):
        save_dir = '../bench_results/raw/many_triples_%s/' % N_TRIPLES
        save_file = save_dir + 'res_many_triples_{n}_{i}.csv'.format(n=N_TRIPLES, i=ind_run)
        bmgr.run(save_file)
