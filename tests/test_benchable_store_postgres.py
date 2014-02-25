from attest import Tests
from ktbs_bench.benchable_store import BenchableStore
import rdflib

BS_POSTGRES = Tests()

# Previously created store are here
CREATED_STORE = {'store_id': 'http://localhost/bs/pg/persistent_store',
                 'config': 'postgresql+psycopg2://localhost/persistent_store'}


@BS_POSTGRES.test
def connect_existing_pg():
    postgres = BenchableStore("SQLAlchemy",
                              CREATED_STORE['store_id'],
                              CREATED_STORE['config'],
                              store_create=False)
    assert postgres.connect() == rdflib.store.VALID_STORE
    postgres.close()


if __name__ == '__main__':
    BS_POSTGRES.run()
