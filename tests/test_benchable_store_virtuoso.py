from uuid import uuid1

import pytest
from ktbs_bench.benchable_graph import BenchableGraph
import rdflib


# This store should be running when running the tests
EMPTY_STORE = {'store_id': 'http://localhost/bs/virtuoso/test/empty_store/',
               'config': ("http://localhost:8890/sparql/", "http://localhost:8890/sparql/")}


class TestVirtuoso:
    def test_fail_connect_query(self):
        """Test that the store should not connect if the query endpoint is wrong."""
        bad_query_endpoint = 'http://should_fail/'
        virtuoso = BenchableGraph("SPARQLUpdateStore",
                                  EMPTY_STORE['store_id'],
                                  (bad_query_endpoint, EMPTY_STORE['config'][1]),
                                  graph_create=False)
        fail = False
        try:
            virtuoso.connect()
            # Doing a query forces RDFLib to actually connect to the query endpoint
            virtuoso.graph.query('select * where {?s ?p ?o}')
        except:
            fail = True
        assert fail

    def test_fail_connect_update(self):
        """Test that the store should not connect if the update endpoint is wrong."""
        bad_update_endpoint = 'http://should_fail'
        virtuoso = BenchableGraph('SPARQLUpdateStore',
                                  EMPTY_STORE['store_id'],
                                  (EMPTY_STORE['config'][0], bad_update_endpoint),
                                  graph_create=False)
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

    def test_succeed_connect(self):
        """Test if the server is up."""
        virtuoso = BenchableGraph('SPARQLUpdateStore',
                                  EMPTY_STORE['store_id'],
                                  EMPTY_STORE['config'],
                                  graph_create=False)
        succeed = True
        try:
            virtuoso.connect()
            virtuoso.graph.query('select * where {?s ?p ?o}')
        except:
            succeed = False
        assert succeed

    @pytest.fixture(scope='module')
    def non_empty_benchable_store(self, request):
        graph_id = 'http://localhost/bs/virtuoso/test/%s' % uuid1()
        virtuoso = BenchableGraph('SPARQLUpdateStore',
                                  graph_id,
                                  ("http://localhost:8890/sparql/", "http://localhost:8890/sparql/"),
                                  graph_create=False)
        virtuoso.connect()

        # Put some triples in the graph
        for i in xrange(10):
            virtuoso.graph.add((rdflib.URIRef('http://localhost/triple/s/%s' % i),
                                rdflib.URIRef('http://localhost/triple/p/%s' % i),
                                rdflib.URIRef('http://localhost/triple/o/%s' % i)))

        # Print action to perform on teardown
        def teardown():
            # TODO should delete the graph from the store
            pass

        request.addfinalizer(teardown)
        return virtuoso

    # Used with non empty graph
    def test_destroy(self, non_empty_benchable_store):
        """Empty a graph, there should be not a single triple in the store after destroy()"""
        # Remove all triples from the store
        non_empty_benchable_store.clear()

        triple_count = len(non_empty_benchable_store.graph)
        assert triple_count == 0
