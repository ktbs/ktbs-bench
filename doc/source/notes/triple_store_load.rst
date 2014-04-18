.. Created 2014-03-04

Load RDF files in triple stores
===============================

How to load rdf files into triple stores?
-----------------------------------------

Virtuoso
~~~~~~~~

Using the ``isql`` command line interface. Then:

::

    DB.DBA.RDF_LOAD_RDFXML_MT (file_to_string_output ('mydata.rdf'), '', 'http://graph_uri');

Note: the virtuoso server must be run in a location parent to the
directory containing ``mydata.rdf``.

Jena
~~~~

Use the cli ``s-put`` as:

::

    s-put {data_store uri} {graph_uri} {data_file}

4-store
~~~~~~~

Use the cli ``4s-import`` as:

::

    4s-import {dataset_name} --model {graph_uri} {data_file}

Note: the http backend (``4s-http``) must not run at the same time.

Other stores (SQLAlchemy, etc.)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``graph.parse()`` from RDFLib.

Note: this doesn't seem to work for Virtuoso.
