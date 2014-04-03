import logging

from ktbs_bench import benchable_graph as bg
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


def get_postgres(db_name, graph_id):
    postgres_store = bg.BenchableGraph(store="SQLAlchemy", graph_id=graph_id,
                                       store_config='postgresql+psycopg2://localhost/%s' % db_name,
                                       graph_create=True)
    return postgres_store


def get_sleepycat(db_path, graph_id, create_graph):
    sleepycat = bg.BenchableGraph(store='Sleepycat', graph_id=graph_id,
                                  store_config=db_path, graph_create=create_graph)
    return sleepycat
