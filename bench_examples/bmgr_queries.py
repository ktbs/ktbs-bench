from random import randint

from ktbs_bench.bench_manager import BenchManager
import sparqlstore


bmgr = BenchManager()


# Making the store contexts
@bmgr.context
def virtuoso():
    rand_graph_id = 'http://localhost/bench/virtuoso/multiple_graph/%s/' % randint(1, 1)
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
def query_sp2b_q5a(graph):
    """Return the names of all persons that occur as author of at least one inproceeding
    and at least one article."""
    graph.query("""
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX dc:    <http://purl.org/dc/elements/1.1/>

        SELECT DISTINCT ?person ?name
        WHERE {
          ?article rdf:type bench:Article .
          ?article dc:creator ?person .
          ?inproc rdf:type bench:Inproceedings .
          ?inproc dc:creator ?person2 .
          ?person foaf:name ?name .
          ?person2 foaf:name ?name2
          FILTER (?name=?name2)
        }
    """)


@bmgr.bench
def query_sp2b_q5b(graph):
    """Return the names of all persons that occur as author of at least one inproceeding
    and at least one article (same as Q5a)."""
    graph.query("""
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX dc:    <http://purl.org/dc/elements/1.1/>

        SELECT DISTINCT ?person ?name
        WHERE {
          ?article rdf:type bench:Article .
          ?article dc:creator ?person .
          ?inproc rdf:type bench:Inproceedings .
          ?inproc dc:creator ?person .
          ?person foaf:name ?name
        }
    """)


@bmgr.bench
def query_sp2b_q6(graph):
    graph.query("""
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT ?yr ?name ?document
        WHERE {
          ?class rdfs:subClassOf foaf:Document .
          ?document rdf:type ?class .
          ?document dcterms:issued ?yr .
          ?document dc:creator ?author .
          ?author foaf:name ?name
          OPTIONAL {
            ?class2 rdfs:subClassOf foaf:Document .
            ?document2 rdf:type ?class2 .
            ?document2 dcterms:issued ?yr2 .
            ?document2 dc:creator ?author2
            FILTER (?author=?author2 && ?yr2<?yr)
          } FILTER (!bound(?author2))
        }
    """)


@bmgr.bench
def query_sp2b_q7(graph):
    """Return the titles of all papers that have been cited at least once,
    but not by any paper that has not been cited itself."""
    graph.query("""
        PREFIX rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs:    <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX foaf:    <http://xmlns.com/foaf/0.1/>
        PREFIX dc:      <http://purl.org/dc/elements/1.1/>
        PREFIX dcterms: <http://purl.org/dc/terms/>

        SELECT DISTINCT ?title
        WHERE {
          ?class rdfs:subClassOf foaf:Document .
          ?doc rdf:type ?class .
          ?doc dc:title ?title .
          ?bag2 ?member2 ?doc .
          ?doc2 dcterms:references ?bag2
          OPTIONAL {
            ?class3 rdfs:subClassOf foaf:Document .
            ?doc3 rdf:type ?class3 .
            ?doc3 dcterms:references ?bag3 .
            ?bag3 ?member3 ?doc
            OPTIONAL {
              ?class4 rdfs:subClassOf foaf:Document .
              ?doc4 rdf:type ?class4 .
              ?doc4 dcterms:references ?bag4 .
              ?bag4 ?member4 ?doc3
            } FILTER (!bound(?doc4))
          } FILTER (!bound(?doc3))
        }
    """)


@bmgr.bench
def query_sp2b_q8(graph):
    graph.query("""
        PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc:   <http://purl.org/dc/elements/1.1/>

        SELECT DISTINCT ?name
        WHERE {
          ?erdoes rdf:type foaf:Person .
          ?erdoes foaf:name "Paul Erdoes"^^xsd:string .
          {
            ?document dc:creator ?erdoes .
            ?document dc:creator ?author .
            ?document2 dc:creator ?author .
            ?document2 dc:creator ?author2 .
            ?author2 foaf:name ?name
            FILTER (?author!=?erdoes &&
                    ?document2!=?document &&
                    ?author2!=?erdoes &&
                    ?author2!=?author)
          } UNION {
            ?document dc:creator ?erdoes.
            ?document dc:creator ?author.
            ?author foaf:name ?name
            FILTER (?author!=?erdoes)
          }
        }
    """)


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


@bmgr.bench
def query_sp2b_q10(graph):
    graph.query("""
        PREFIX person: <http://localhost/persons/>

        SELECT ?subject ?predicate
        WHERE {
          ?subject ?predicate person:Paul_Erdoes
        }
    """)


@bmgr.bench
def query_sp2b_q11(graph):
    graph.query("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT ?ee
        WHERE {
          ?publication rdfs:seeAlso ?ee
        }
        ORDER BY ?ee
        LIMIT 10
        OFFSET 50
    """)


@bmgr.bench
def query_sp2b_q12a(graph):
    graph.query("""
        PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf:  <http://xmlns.com/foaf/0.1/>
        PREFIX bench: <http://localhost/vocabulary/bench/>
        PREFIX dc:    <http://purl.org/dc/elements/1.1/>

        ASK {
          ?article rdf:type bench:Article .
          ?article dc:creator ?person1 .
          ?inproc  rdf:type bench:Inproceedings .
          ?inproc  dc:creator ?person2 .
          ?person1 foaf:name ?name1 .
          ?person2 foaf:name ?name2
          FILTER (?name1=?name2)
        }
    """)


@bmgr.bench
def query_sp2b_q12b(graph):
    graph.query("""
        PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
        PREFIX rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc:   <http://purl.org/dc/elements/1.1/>

        ASK {
          ?erdoes rdf:type foaf:Person .
          ?erdoes foaf:name "Paul Erdoes"^^xsd:string .
          {
            ?document dc:creator ?erdoes .
            ?document dc:creator ?author .
            ?document2 dc:creator ?author .
            ?document2 dc:creator ?author2 .
            ?author2 foaf:name ?name
            FILTER (?author!=?erdoes &&
                    ?document2!=?document &&
                    ?author2!=?erdoes &&
                    ?author2!=?author)
          } UNION {
            ?document dc:creator ?erdoes .
            ?document dc:creator ?author .
            ?author foaf:name ?name
            FILTER (?author!=?erdoes)
          }
        }
    """)


@bmgr.bench
def query_sp2b_q12c(graph):
    graph.query("""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX person: <http://localhost/persons/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>

    ASK {
      person:John_Q_Public rdf:type foaf:Person.
    }
    """)


if __name__ == '__main__':
    bmgr.run('/tmp/none.csv')
