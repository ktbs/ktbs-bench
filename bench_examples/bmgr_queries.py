from random import randint

from ktbs_bench.bench_manager import BenchManager
import sparqlstore


bmgr = BenchManager()


# Making the store contexts
@bmgr.context
def virtuoso():
    rand_graph_id = 'http://localhost/bench/virtuoso/multiple_graph/%s/' % randint(1, 10)
    bs_virtuoso = sparqlstore.get_sparqlstore("http://localhost:8890/sparql/", "http://localhost:8890/sparql/",
                                              identifier=rand_graph_id)
    try:
        # The stuff we want to do before executing the bench function
        bs_virtuoso.connect()
        n_triples = len(bs_virtuoso.graph)
        assert 32000 < n_triples < 33000
        # Yield the object the bench function needs
        yield bs_virtuoso.graph
    finally:
        # Stuff to do after we executed the bench function
        bs_virtuoso.close()
    del bs_virtuoso


@bmgr.bench
def query_all(graph):
    graph.query('select * where {?s ?p ?o}')


@bmgr.bench
def query_sp2b_q1(graph):
    """Return the year of publication of "Journal 1 (1940)".

    This simple query returns exactly one result (for arbitrarily
    large documents). Native engines might use index lookups
    in order to answer this query in (almost) constant time,
    i.e. execution time should be independent from document size.
    (From SP2BENCH Tech Report)
    """
    graph.query("""
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX bench:   <http://localhost/vocabulary/bench/>
        PREFIX xsd:     <http://www.w3.org/2001/XMLSchema#>

        SELECT ?yr
        WHERE {
          ?journal rdf:type bench:Journal .
          ?journal dc:title "Journal 1 (1940)"^^xsd:string .
          ?journal dcterms:issued ?yr
        }""")


@bmgr.bench
def query_sp2b_q2(graph):
    """
    This query implements a bushy graph pattern. It contains
    a single, simple OPTIONAL expression, and accesses large
    strings (i.e. the abstracts). Result size grows with database
    size, and a final result ordering is necessary due to operator
    ORDER BY. Both native and in-memory engines might reach
    evaluation times that are almost linear to the document size.
    (From SP2BENCH Tech Report)
    """
    graph.query("""
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX swrc:    <http://swrc.ontoware.org/ontology#>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX bench:   <http://localhost/vocabulary/bench/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT ?inproc ?author ?booktitle ?title
               ?proc ?ee ?page ?url ?yr ?abstract
        WHERE {
          ?inproc rdf:type bench:Inproceedings .
          ?inproc dc:creator ?author .
          ?inproc bench:booktitle ?booktitle .
          ?inproc dc:title ?title .
          ?inproc dcterms:partOf ?proc .
          ?inproc rdfs:seeAlso ?ee .
          ?inproc swrc:pages ?page .
          ?inproc foaf:homepage ?url .
          ?inproc dcterms:issued ?yr
          OPTIONAL {
            ?inproc bench:abstract ?abstract
          }
        }
        ORDER BY ?yr""")


@bmgr.bench
def query_sp2b_q3a(graph):
    """Select all articles with property swrc:pages

    This query tests FILTER expressions with varying selectivity.
    According to Table I, the FILTER expression in Q3a is not
    very selective (i.e. retains about 92.61% of all articles). Data
    access through a secondary index for Q3a is probably not very
    efficient, but might work well for Q3b, which selects only
    0.65% of all articles. The filter condition in Q3c
    is never satisfied, as no articles have swrc:isbn predicates. Schema
    statistics might be used to answer Q3c in constant time.
    (From SP2BENCH Tech Report)
    """
    graph.query("""
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX swrc:  <http://swrc.ontoware.org/ontology#>

        SELECT ?article
        WHERE {
          ?article rdf:type bench:Article .
          ?article ?property ?value
          FILTER (?property=swrc:pages)
        }""")


@bmgr.bench
def query_sp2b_q3b(graph):
    """Select all articles with property swrc:month"""
    graph.query("""
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX swrc:  <http://swrc.ontoware.org/ontology#>

        SELECT ?article
        WHERE {
          ?article rdf:type bench:Article .
          ?article ?property ?value
          FILTER (?property=swrc:month)
        }""")


@bmgr.bench
def query_sp2b_q3c(graph):
    """Select all articles with property swrc:isbn."""
    graph.query("""
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX swrc:  <http://swrc.ontoware.org/ontology#>
        PREFIX bench: <http://localhost/vocabulary/bench/>

        SELECT ?article
        WHERE {
          ?article rdf:type bench:Article .
          ?article ?property ?value
          FILTER (?property=swrc:isbn)
        }""")


@bmgr.bench
def query_sp2b_q4(graph):
    """
    Select all distinct pairs of article author names for authors
    that have published in the same journal.

    Q4 contains a rather long graph chain, i.e. variables ?name1 and ?name2
    are linked through the articles the authors have
    published, and a common journal. The result is very large,
    basically quadratic in number and size of journals. Instead
    of evaluating the outer pattern block and applying the FILTER
    afterwards, engines might embed the FILTER expression in the
    computation of the block, e.g. by exploiting indices on auth
    or names. The DISTINCT modifier further complicates the query.
    We expect superlinear behavior, even for native engines.
    (From SP2BENCH Tech Report)
    """
    graph.query("""
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX bench:   <http://localhost/vocabulary/bench/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX swrc:    <http://swrc.ontoware.org/ontology#>

        SELECT DISTINCT ?name1 ?name2
        WHERE {
          ?article1 rdf:type bench:Article .
          ?article2 rdf:type bench:Article .
          ?article1 dc:creator ?author1 .
          ?author1 foaf:name ?name1 .
          ?article2 dc:creator ?author2 .
          ?author2 foaf:name ?name2 .
          ?article1 swrc:journal ?journal .
          ?article2 swrc:journal ?journal
          FILTER (?name1<?name2)
        }""")


@bmgr.bench
def query_sp2b_q9(graph):
    """Return incoming and outgoing properties of persons.

    Q9 has been designed to test non-standard data access patterns.
    Naive implementations would compute the triple patterns
    of the UNION subexpressions separately, thus evaluate patterns
    where no component is bound. Then, pattern
    ?subject ?predicate ?person would select all graph
    triples, which is rather inefficient. Another idea is to evaluate
    the first triple in each UNION subexpression, afterwards using
    the bindings for variable ?person to evaluate the second patterns
    more efficiently. In this case, we observe patterns where only the
    subject (resp. the object) is bound. Also observe
    that this query extracts schema information. The result size
    is exactly 4 (for sufficiently large documents). Statistics about
    incoming/outgoing properties of Person-typed objects in native
    engines might be used to answer this query in constant time,
    even without data access. In-memory engines always must load
    the document, hence might scale linearly to document size.
    (From SP2BENCH Tech Report)
    """
    graph.query("""
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>

        SELECT DISTINCT ?predicate
        WHERE {
          {
            ?person rdf:type foaf:Person .
            ?subject ?predicate ?person
          } UNION {
            ?person rdf:type foaf:Person .
            ?person ?predicate ?object
          }
        }
    """)


if __name__ == '__main__':
    for ind_file in xrange(20):
        bmgr.run('/tmp/res_bmgr_10graph_' + str(ind_file) + '.csv')
