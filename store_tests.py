# -*- coding: utf-8 -*-

import utils
import rdflib as r
from rdflib import RDF
from bz2 import BZ2File


def iter_insert(n_insert, graph):
    """Insert many triples in a graph store."""
    times = [0, 0]

    for ind_insert in xrange(n_insert):
        subj = r.URIRef("http://localhost/multi_insert/subject/%s" % ind_insert)
        pred = RDF.type
        obj = r.URIRef("http://localhost/multi_insert/object/%s" % ind_insert)

        tstart = utils.clock2()
        graph.add((subj, pred, obj))
        tend = utils.clock2()

        utils.add_delta_time(times, tstart, tend)

    return times


def batch_insert(bz2file, graph, file_format="n3"):
    """Insert many triples in a graph store at once.

    For better accuracy, the parsing is done separately.
    The triples are in memory before adding them to the store.
    """
    data_file = BZ2File(bz2file)

    memory_graph = r.Graph()
    memory_graph.parse(data_file, format=file_format)

    tstart = utils.clock2()
    graph += memory_graph
    tend = utils.clock2()

    return [end - start for start, end in zip(tstart, tend)]
