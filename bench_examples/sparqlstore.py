from ktbs_bench.benchable_store import BenchableStore
import rdflib

rdflib.plugin.register('BN', rdflib.store.Store, 'ktbs_bench.bnsparqlstore', 'SPARQLUpdateStore')


def get_sparqlstore(query_endpoint, update_endpoint, identifier="http://localhost/generic_sparqlstore/"):
    triple_store = BenchableStore(store='BN', graph_id=identifier,
                                  store_config=(query_endpoint, update_endpoint))
    return triple_store
