from csv import DictWriter

import rdflib as r
from ktbs_bench.utils.decorators import bench


@bench
def batch_insert(graph, file):
    """Insert triples in batch WITH PARSING."""
    graph.parse(file, format="rdfa")


@bench
def query_all(graph):
    graph.query('select * where {?s ?p ?o}')


@bench
def query_sp2b_q1(graph):
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


@bench
def query_sp2b_q2(graph):
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


@bench
def query_sp2b_q3a(graph):
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


@bench
def query_sp2b_q3b(graph):
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


@bench
def query_sp2b_q3c(graph):
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


@bench
def query_sp2b_q4(graph):
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


@bench
def query_sp2b_q9(graph):
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
    # Define some graph/store to use
    import nosparqlstore
    import sparqlstore

    r.plugin.register('BN', r.store.Store, 'ktbs_bench.bnsparqlstore', 'SPARQLUpdateStore')

    virtuoso = sparqlstore.get_sparqlstore("http://localhost:8890/sparql/", "http://localhost:8890/sparql/",
                                           identifier="http://localhost/virtuoso/1")

    _4store = sparqlstore.get_sparqlstore("http://localhost:8000/sparql/", "http://localhost:8000/update/",
                                          identifier="http://localhost/4store/1")

    jena = sparqlstore.get_sparqlstore("http://localhost:3030/ds/query", "http://localhost:3030/ds/update",
                                       identifier="http://localhost/jena/1")

    postgres = nosparqlstore.get_postgres("db_benchtest", "vincent")
    postgres.create()

    sleepycat = nosparqlstore.get_sleepycat('/tmp/sc.db')
    sleepycat.create()

    graph_dict = {'virtuoso': virtuoso, '4store': _4store, 'jena': jena, 'postgres': postgres, 'sleepycat': sleepycat}

    # Print graph size
    print("size of graph before inserts")
    for graph_name, graph in graph_dict.items():
        graph.connect()
        print("%s: %s" % (graph_name, len(graph)))
        graph.close()

    # Define some files to get the triples from
    n3file_list = ['../data/32000.rdfa']

    csv_columns = set()

    # Creating clean data
    for graph in graph_dict.values():
        for n3file in n3file_list:
            graph.connect()
            batch_insert(graph, n3file)
            graph.close()

    # Testing query
    all_res = []
    for query_func in [query_all, query_sp2b_q1, query_sp2b_q2, query_sp2b_q3a, query_sp2b_q3b, query_sp2b_q3c,
                       query_sp2b_q4, query_sp2b_q9]:
        func_res = {'func_name': query_func.__name__}
        for graph_name, graph in graph_dict.items():
            graph.connect()
            time_res = query_func(graph)
            func_res[graph_name] = time_res[1]
            csv_columns.add(graph_name)
            graph.close()

        all_res.append(func_res)

    # Store teardown
    for store in graph_dict.values():
        store.destroy()

    # Setup the result CSV
    with open('/tmp/res3_32000.csv', 'wb') as outfile:
        res_csv = DictWriter(outfile, fieldnames=['func_name'] + list(csv_columns))
        res_csv.writeheader()

        # Write the results
        res_csv.writerows(all_res)
