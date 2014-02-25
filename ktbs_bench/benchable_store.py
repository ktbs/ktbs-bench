import logging

from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from ktbs_bench.bnsparqlstore import SPARQLStore as bn_SPARQLStore


class BenchableStore:
    """Allows to use a store/graph for benchmarks.

    Contains a rdflib.Graph with setup and teardown.
    """

    def __init__(self, store, graph_id, store_config, store_create=False):
        self.graph = Graph(store=store, identifier=graph_id)
        self._graph_id = graph_id
        self._store_config = store_config
        self._store_create = store_create

    def connect(self):
        return self.graph.open(configuration=self._store_config, create=self._store_create)

    def close(self, commit_pending_transaction=False):
        self.graph.close(commit_pending_transaction=commit_pending_transaction)

    def destroy(self):
        if isinstance(self.graph.store, bn_SPARQLStore) \
                or isinstance(self.graph.store, SPARQLStore):
            self.empty_sparql()
        else:
            self.graph.destroy(self._store_config)

    def empty_sparql(self):
        """Try to destroy the graph as if the current store is a SPARQLStore."""
        try:
            self.graph.update("""
            DELETE FROM GRAPH <%s> {?s ?p ?o}
            WHERE { GRAPH <%s> {?s ?p ?o} }
            """ % (self._graph_id, self._graph_id))
        except:
            logging.info("Clearing graph with graph.update() didn't work, now removing items one by one.")
            for s, p, o in self.graph:
                self.graph.remove((s, p, o))
