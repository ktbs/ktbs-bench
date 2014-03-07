import logging

from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from ktbs_bench.bnsparqlstore import SPARQLStore as bn_SPARQLStore


class BenchableGraph:
    """
    Provides a convenient way to use a graph for benchmarks.

    """
    def __init__(self, store, graph_id, store_config, graph_create=False):
        """
        :param store: Type of store to use.
        :type store: str
        :param graph_id: The graph identifier.
        :type graph_id: str
        :param store_config: Configuration to open the store.
        :type store_config: str, tuple
        :param graph_create: True to create the graph upon connecting.
        :type graph_create: bool
        """
        self.graph = Graph(store=store, identifier=graph_id)
        self._graph_id = graph_id
        self._store_config = store_config
        self._graph_create = graph_create

    def connect(self):
        """Connect to the store.

        For some configurations, the connection is postponed until needed
        (e.g. when doing a graph.query() or graph.add()).
        This behaviour comes from RDFLib implementation of graph.open().
        """
        return self.graph.open(configuration=self._store_config, create=self._graph_create)

    def close(self, commit_pending_transaction=True):
        """Close a connection to a store.

        :param commit_pending_transaction: True if to commit pending transaction before closing, False otherwise.
        :type commit_pending_transaction: bool

        .. note::
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
