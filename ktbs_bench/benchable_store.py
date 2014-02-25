from rdflib import Graph
from ktbs_bench.bnsparqlstore import SPARQLStore


class BenchableStore:
    """Allows to use a store/graph for benchmarks.

    Contains a rdflib.Graph with setup and teardown.
    """

    def __init__(self, store, graph_id, store_config, store_create=False):
        self.graph = Graph(store=store, identifier=graph_id)
        self._store_config = store_config
        self._store_create = store_create

    def connect(self, store_create=None):
        if store_create:
            do_create = store_create
        else:
            do_create = self._store_create
        self.graph.open(self._store_config, create=do_create)

    def close(self, commit_pending_transaction=False):
        self.graph.close(commit_pending_transaction=commit_pending_transaction)

    def destroy(self):
        if isinstance(self.graph.store, SPARQLStore):
            self.sparql_destroy()
        else:
            self.graph.destroy(self._store_config)

    def sparql_destroy(self):
        """Try to destroy the graph as if the current store is a SPARQLStore."""
        # TODO improve destroy by using SPARQL CLEAR GRAPH if RDFLib supports it
        # or execute something on the command line
        for s, p, o in self.graph:
            self.graph.remove((s, p, o))
