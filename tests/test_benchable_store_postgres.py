from ktbs_bench.benchable_graph import BenchableGraph
import rdflib


# Previously created store are here
CREATED_STORE = {'store_id': 'http://localhost/bs/pg/persistent_store',
                 'config': 'postgresql+psycopg2://localhost/persistent_store'}


def test_connect_existing_pg():
    postgres = BenchableGraph("SQLAlchemy",
                              CREATED_STORE['store_id'],
                              CREATED_STORE['config'],
                              graph_create=False)
    assert postgres.connect() == rdflib.store.VALID_STORE
    postgres.close()
