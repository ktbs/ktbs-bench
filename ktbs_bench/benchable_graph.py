import logging

from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from ktbs_bench.bnsparqlstore import SPARQLStore as bn_SPARQLStore


class BenchableGraph:
    """
    Provides a convenient way to use a graph for benchmarks.

    """

    def __init__(self, store, graph_id, store_config, store_create=False):
        self.graph = Graph(store=store, identifier=graph_id)
        self._graph_id = graph_id
        self._store_config = store_config
        self._store_create = store_create

    def connect(self):
        """Connect to the store.

        For some configurations, the connection is postponed until needed
        (e.g. when doing a graph.query() or graph.add()).
        This behaviour is part of RDFLib.
        """
        return self.graph.open(configuration=self._store_config, create=self._store_create)

    def close(self, commit_pending_transaction=True):
        """Close a connection to a store.

        Note (2014-03-07):
            The graph.close() method is not implemented for SPARQL Store in RDFLib
        """
        self.graph.close(commit_pending_transaction=commit_pending_transaction)

    def clear(self):
        """Delete all triples of the current graph."""
        # Helper function that removes triples by iterating over them
        def clear_one_by_one():
            for s, p, o in self.graph:
                self.graph.remove((s, p, o))

        # SPARQL graph
        if isinstance(self.graph.store, bn_SPARQLStore) or isinstance(self.graph.store, SPARQLStore):
            try:
                self.clear_graph_sparql()
            except:
                logging.info("Clearing graph with graph.update() didn't work, now removing items one by one.")
                clear_one_by_one()
        # Other graph (SQL, etc.)
        else:
            clear_one_by_one()

    def clear_graph_sparql(self):
        """Clear graph by using a SPARQL update query.

        This is more efficient than iterating over every triple in the store
        and deleting them using RDFLib.
        """
        self.graph.update("""
        DELETE FROM GRAPH <%s> {?s ?p ?o}
        WHERE { GRAPH <%s> {?s ?p ?o} }
        """ % (self._graph_id, self._graph_id))
