import rdflib
from sutils import fork

from ktbs_bench.bench_manager import BenchManager
import nosparqlstore
import queries


bmgr = BenchManager(set_log_info=True)

rdflib.plugin.register('BN', rdflib.store.Store, 'ktbs_bench.bnsparqlstore', 'SPARQLUpdateStore')
VIRT = {'store': 'BN',
        'id_sub': 'virtuoso',
        'open': ('http://localhost:8890/sparql/', 'http://localhost:8890/sparql/')}
PG = {'store': 'SQLAlchemy',
      'id_sub': 'postgres',
      'open': 'postgresql+psycopg2://localhost/many_graph'}
SLEEPY = {'store': 'Sleepycat',
          'id_sub': 'sleepy',
          'open': '/home/vincent/projets/liris/ktbs_bench/sleepycat_many_triples_1m_triples'}

CHECK_BACKENDS = {'sleepy': SLEEPY}
N_RUN = 10
MIN_TRIPLES = 1024000
MAX_TRIPLES = 1024200
BENCH_NAME = '1m_triples'


@bmgr.context
def sleepycat():
    graph_prefix = 'http://localhost/bench/sleepy/%s/' % BENCH_NAME
    bs_sleepycat = nosparqlstore.get_sleepycat(SLEEPY['open'], graph_prefix)
    try:
        # Checking number of triples in graph
        bs_sleepycat.connect()
        n_triples = len(bs_sleepycat.graph)
        assert MIN_TRIPLES < n_triples < MAX_TRIPLES
        bs_sleepycat.close()
        bmgr.get_logger().info(
            'Sleepycat graph {graph_id} checked for {min} < {n} < {max}'.format(graph_id=bs_sleepycat.graph.identifier,
                                                                                min=MIN_TRIPLES,
                                                                                n=n_triples,
                                                                                max=MAX_TRIPLES))
        yield bs_sleepycat
    finally:
        pass
    del bs_sleepycat


@bmgr.bench
@fork(n=3)
def queries_cocktail(benchable_graph):
    benchable_graph.connect()
    print('fork')
    for _ in xrange(50):
        benchable_graph.graph.query(queries.QUERIES['query_all'])
        benchable_graph.graph.query(queries.QUERIES['q1'])
        benchable_graph.graph.query(queries.QUERIES['q3a'])
        benchable_graph.graph.query(queries.QUERIES['q3b'])
        benchable_graph.graph.query(queries.QUERIES['q3c'])
        benchable_graph.graph.query(queries.QUERIES['q4'])
        benchable_graph.graph.query(queries.QUERIES['q5a'])
        benchable_graph.graph.query(queries.QUERIES['q5b'])
        benchable_graph.graph.query(queries.QUERIES['q6'])
        benchable_graph.graph.query(queries.QUERIES['q7'])
        benchable_graph.graph.query(queries.QUERIES['q8'])
        benchable_graph.graph.query(queries.QUERIES['q9'])
        benchable_graph.graph.query(queries.QUERIES['q10'])
        benchable_graph.graph.query(queries.QUERIES['q11'])
        benchable_graph.graph.query(queries.QUERIES['q12c'])
    benchable_graph.close()


if __name__ == '__main__':
    # Run the benchs
    for ind_run in xrange(N_RUN):
        save_dir = '/home/vincent/projets/liris/ktbs_bench/bench_results/raw/one_graph_1m_triples_3forks/'
        save_file = save_dir + 'res_q1m_{i}.csv'.format(i=ind_run)
        bmgr.run(save_file)
