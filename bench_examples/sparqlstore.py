from ktbs_bench_manager import BenchableGraph
import rdflib

rdflib.plugin.register('BN', rdflib.store.Store, 'rdflib.plugins.stores.bnsparqlstore', 'SPARQLUpdateStore')


def get_sparqlstore(query_endpoint, update_endpoint, identifier="http://localhost/generic_sparqlstore/"):
    triple_store = BenchableGraph(store='BN', graph_id=identifier,
                                  store_config=(query_endpoint, update_endpoint))
    return triple_store
