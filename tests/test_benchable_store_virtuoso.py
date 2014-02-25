from attest import Tests
from ktbs_bench.benchable_store import BenchableStore
import rdflib

BS_VIRTUOSO = Tests()

# Previously created store are here
CREATED_STORE = {'store_id': 'http://localhost/bs/virtuoso/persistent_store',
                 'config': ("http://localhost:8890/sparql/", "http://localhost:8890/sparql/")}


@BS_VIRTUOSO.test
def fail_query():
    bad_query_endpoint = 'http://should_fail/'
    virtuoso = BenchableStore("SPARQLUpdateStore",
                              CREATED_STORE['store_id'],
                              (bad_query_endpoint, CREATED_STORE['config'][1]),
                              store_create=False)
    fail = False
    try:
        virtuoso.connect()
        virtuoso.graph.query('select * where {?s ?p ?o}')
    except:
        fail = True
    assert fail


@BS_VIRTUOSO.test
def succeed_connect():
    virtuoso = BenchableStore('SPARQLUpdateStore',
                              CREATED_STORE['store_id'],
                              CREATED_STORE['config'],
                              store_create=False)
    succeed = True
    try:
        virtuoso.connect()
        virtuoso.graph.query('select * where {?s ?p ?o}')
    except:
        succeed = False
    assert succeed


@BS_VIRTUOSO.test
def fail_update():
    bad_update_endpoint = 'http://should_fail'
    virtuoso = BenchableStore('SPARQLUpdateStore',
                              CREATED_STORE['store_id'],
                              (CREATED_STORE['config'][0], bad_update_endpoint),
                              store_create=False)
    fail = False
    try:
        virtuoso.connect()
        virtuoso.graph.add((rdflib.URIRef('s'), rdflib.URIRef('p'), rdflib.URIRef('o')))
    except:
        fail = True
    assert fail


@BS_VIRTUOSO.test
def test_destroy():
    virtuoso = BenchableStore('SPARQLUpdateStore',
                              CREATED_STORE['store_id'],
                              CREATED_STORE['config'],
                              store_create=False)
    virtuoso.connect()

    # Adding a triple to the store, so it has at least one
    virtuoso.graph.add((rdflib.URIRef('s'), rdflib.URIRef('p'), rdflib.URIRef('o')))

    # Remove all triples from the store
    virtuoso.destroy()

    triple_count = len(virtuoso.graph)
    assert triple_count == 0


if __name__ == '__main__':
    BS_VIRTUOSO.run()
