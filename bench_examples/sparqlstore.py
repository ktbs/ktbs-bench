from ktbs_bench.benchable_store import BenchableStore
import rdflib

rdflib.plugin.register('BN', rdflib.store.Store, 'ktbs_bench.bnsparqlstore', 'SPARQLUpdateStore')


def get_sparqlstore(query_endpoint, update_endpoint, identifier="http://localhost/generic_sparqlstore/"):
    triple_store = BenchableStore(store='BN', identifier=identifier,
                                  connect_args={'configuration': (query_endpoint, update_endpoint)})
    return triple_store
