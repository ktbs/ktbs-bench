# -*- coding:utf-8 -*-

from os import listdir
from bz2 import BZ2File
import rdflib as r
import psycopg2 as pg
import time
import re
import logging


class BenchStore:
    def __init__(self, name, config, create_db_func=None, create_db_args=[]):
        self.name = name
        self.config = config
        self.create_db_func = create_db_func
        self.create_db_args = create_db_args


    def __repr__(self):
        return "%s [%s]" % (self.name, self.config)


    def create(self):
        """Things to do to create the store."""
        if self.create_db_func is not None:
            try:
                # Run create_db_func with the argument list create_db_args
                self.create_db_func(*self.create_db_args)
            except Exception, e:
                logging.warning("An error occured during database creation, continuing. %s" % e)

        g = r.Graph(self.name)
        g.open(self.config, create=True)
        g.close()


    def destroy(self, graph):
        graph.destroy(self.config)


def bench(stores, datadir, outfile=None):
    """Benchmark different stores against some data.

    Arguments:
    - stores: a dictionnary of stores to use for RDFlib
    - datadir: a directory containing data files (must be .n3.bz2 for now)
    - outfile: output a CSV file (not for now)
    """
    for store in stores:
        files = filter(lambda f: f.endswith('.n3.bz2'), listdir(datadir))
        files.sort(key=natural_keys)

        for fcomp in files[:5]:
            f = BZ2File(datadir + fcomp)  # decompress file, returns a file object

            # Create the database
            store.create()

            # Setting the graph with database info
            g = r.ConjunctiveGraph(store.name)
            g.open(store.config, create=False)

            # Benchmarking: parse and add the data to the graph
            tstart = time.clock()
            g.parse(source=f, format='n3')
            g.commit()
            print("file: %s\tDB: %s\tconfig: %s\ttime: %ss" % (fcomp, store.name,
                                                               store.config,
                                                               time.clock() - tstart))

            # Destroy the tables
            store.destroy(g)
            g.close()


def natural_keys(text):
    def cast(text):
        return int(text) if text.isdigit() else text

    return [cast(text_block) for text_block in re.split('(\d+)', text)]


def pg_create(db_name, db_user):
    """Create a PostgreSQL database."""
    connection = pg.connect("dbname=%s user=%s" % (db_user, db_user))  # connect to db_user as db_name has not been created yet
    connection.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE %s" % db_name)
    cursor.close()
    connection.close()


if __name__ == '__main__':
    # Register the store plugins
    from rdflib_sqlalchemy import registerplugins
    registerplugins()

    r.plugin.register('PostgreSQL', r.store.Store, 'rdflib_postgresql.PostgreSQL', 'PostgreSQL')
    r.plugin.register('SQLite', r.store.Store, 'rdflib_sqlite.SQLite', 'SQLite')

    # Set up the store for rdflib
    sqla_pg = BenchStore('SQLAlchemy', 'postgresql+psycopg2://localhost/newtest_sqapg', pg_create, ["newtest_sqapg", "vincent"])
    sqla_sqlite = BenchStore('SQLAlchemy', 'sqlite:////tmp/t.db')
    postgres = BenchStore('PostgreSQL', 'user=vincent dbname=newtest_pg', pg_create, ["newtest_pg", "vincent"])
    slite = BenchStore('SQLite', '/tmp/t2.db')
    stores = [slite, sqla_sqlite]

    datadir = 'data/'

    bench(stores, datadir)

