import logging

from ktbs_bench import benchable_store as bs
import psycopg2 as pg


def pg_create(db_name, db_user):
    """Create a PostgreSQL database."""
    connection = pg.connect(
        "dbname=%s user=%s" % (db_user, db_user))  # connect to db_user as db_name might not been created yet
    connection.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    try:
        cursor.execute("CREATE DATABASE %s" % db_name)
    except pg.ProgrammingError:
        logging.warning("An error occurred during database creation, trying to continue without creating a new one.")

    cursor.close()
    connection.close()


def get_postgres(db_name, db_user):
    postgres_store = bs.BenchableStore(store="SQLAlchemy",
                                       connect_args={'configuration': "postgresql+psycopg2://localhost/%s" % db_name,
                                                     'create': True},
                                       create_func=pg_create, create_args=[db_name, db_user])
    return postgres_store


def get_sleepycat(db_path):
    sleepycat = bs.BenchableStore(store='Sleepycat',
                                  connect_args={'configuration': db_path, 'create': True})
    return sleepycat