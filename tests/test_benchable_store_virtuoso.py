from uuid import uuid1

from attest import Tests
from ktbs_bench.benchable_store import BenchableStore
import rdflib


VIRTUOSO_CONNECT = Tests()
EMPTY_STORE = {'store_id': 'http://localhost/bs/virtuoso/test/empty_store/',
               'config': ("http://localhost:8890/sparql/", "http://localhost:8890/sparql/")}

VIRTUOSO_NOT_EMPTY = Tests()


@VIRTUOSO_CONNECT.test
def fail_connect_query():
    """Test that the store should not connect if the query endpoint is wrong."""
    bad_query_endpoint = 'http://should_fail/'
    virtuoso = BenchableStore("SPARQLUpdateStore",
                              EMPTY_STORE['store_id'],
                              (bad_query_endpoint, EMPTY_STORE['config'][1]),
                              store_create=False)
    fail = False
    try:
        virtuoso.connect()
        # Doing a query forces RDFLib to actually connect to the query endpoint
        virtuoso.graph.query('select * where {?s ?p ?o}')
    except:
        fail = True
    assert fail


@VIRTUOSO_CONNECT.test
def fail_connect_update():
    """Test that the store should not connect if the update endpoint is wrong."""
    bad_update_endpoint = 'http://should_fail'
    virtuoso = BenchableStore('SPARQLUpdateStore',
                              EMPTY_STORE['store_id'],
                              (EMPTY_STORE['config'][0], bad_update_endpoint),
                              store_create=False)
    fail = False
    triple = (rdflib.URIRef('s'), rdflib.URIRef('p'), rdflib.URIRef('o'))
    try:
        virtuoso.connect()
        # Doing an add forces RDFLib to actually connect to the update endpoint
        virtuoso.graph.add(triple)
    except:
        fail = True
    else:
        virtuoso.graph.remove(triple)
    assert fail


@VIRTUOSO_CONNECT.test
def succeed_connect():
    """Test if the server is up."""
    virtuoso = BenchableStore('SPARQLUpdateStore',
                              EMPTY_STORE['store_id'],
                              EMPTY_STORE['config'],
                              store_create=False)
    succeed = True
    try:
        virtuoso.connect()
        virtuoso.graph.query('select * where {?s ?p ?o}')
    except:
        succeed = False
    assert succeed


@VIRTUOSO_NOT_EMPTY.context
def connect():
    try:
        virtuoso = BenchableStore('SPARQLUpdateStore',
                                  'http://localhost/bs/virtuoso/test/%s' % uuid1(),
                                  ("http://localhost:8890/sparql/", "http://localhost:8890/sparql/"),
                                  store_create=False)
        virtuoso.connect()

        # Put some triples in the graph
        for i in xrange(100):
            virtuoso.graph.add((rdflib.URIRef('http://localhost/triple/s/%s' % i),
                                rdflib.URIRef('http://localhost/triple/p/%s' % i),
                                rdflib.URIRef('http://localhost/triple/o/%s' % i)))
        yield virtuoso
    finally:
        pass  # Could have use close(), but not implemented for SPARQL store in RDFLib


@VIRTUOSO_NOT_EMPTY.test
def test_destroy(benchable_store):
    """Empty a graph, there should be not a single triple in the store after destroy()"""
    # Remove all triples from the store
    benchable_store.destroy()

    triple_count = len(benchable_store.graph)
    assert triple_count == 0


if __name__ == '__main__':
    VIRTUOSO_CONNECT.run()
    VIRTUOSO_NOT_EMPTY.run()
