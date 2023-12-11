########################
Arches and Elasticsearch
########################

Arches uses `Elasticsearch <https://www.elastic.co/elasticsearch/>`_ as its search engine. A handful of ``settings.py`` variables point your Arches project to an Elasticsearch installation, in which your indexes will be created. An ``ELASTICSEARCH_PREFIX`` string is prepended to all of your project's indexes, meaning that a single Elasticsearch installation can be used by multiple projects.

One important thing to remember: **Elasticsearch indexes are replicable derivatives of your Arches database**, meaning that they can safely be dropped and recreated at any time. Similarly, if you need to change or upgrade your Elasticsearch setup, you need only update some settings and then reindex your database.

You can install Elasticsearch locally alongside Arches--read on for how to do that. You can also use managed Elasticsearch solutions by cloud providers like `AWS <https://aws.amazon.com/what-is/elasticsearch/>`_.

Installing Elasticsearch
========================

The easiest way to install Elasticsearch is to download and unpack their archived releases. Archives are available at ``https://www.elastic.co/downloads/past-releases/elasticsearch-{release number}``, e.g. https://www.elastic.co/downloads/past-releases/elasticsearch-8-5-1.

Download the release for your OS and architecture and then unpack/unzip it. For example, installing 8.5.1 on Ubuntu Linux looks like:

.. code-block:: shell

    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.5.1-linux-x86_64.tar.gz
    tar -zxvf elasticsearch-8.5.1-linux-x86_64.tar.gz

A full installation is now in ``./elasticsearch-8.5.1``, which you can start by running ``./elasticsearch-8.5.1/bin/elasticsearch`` (see below).

On Windows you will need the Windows release which is a ZIP archive, but the process is basically the same.

Development Configuration
=========================

Elasticsearch 8 introduced new security features. While you are working with Arches locally, i.e. during development, you can safely disable these features. *Do not disable security features in production.*

Make two changes:

1. In your config file, find ``xpack.security.enabled = true`` and set it to ``xpack.security.enabled = false``. Now start/restart Elasticsearch (see below).

    The config file is typically found at ``{path-to-elasticsearch}\config\elasticsearch.yml``. If you installed the Debian package, you'll find it at ``/etc/elasticsearch/elasticsearch.yml``.

2. In your Arches project's ``settings.py`` or ``settings_local.py``, add

    .. code-block:: python

        ELASTICSEARCH_HOSTS = [{'scheme': 'http', 'host': 'localhost', 'port': ELASTICSEARCH_HTTP_PORT}]

    This overwrites the default ``ELASTICSEARCH_HOSTS`` variable, which has the scheme set to ``https``.

Running Elasticsearch
=====================

**Linux/macOS**:

After unpacking the archive, use

.. code-block:: shell

   {path-to-elasticsearch}/bin/elasticsearch

To rum in the background, add ``-d`` to that command. To stop the background process, use ``ps aux | grep elasticsearch`` to get the process id, and then ``sudo kill <process id> -9``.

**Windows**:

On Windows, double-click the ``{path-to-elasticsearch}\bin\elasticsearch.bat`` batch file to run the process in a new console window.

---------------------------------------------------------

To make sure Elasticsearch is running correctly, use

.. code-block:: bash

    curl localhost:9200

You should get a JSON response that includes "You Know, For Search...". You can also use the Chrome plugin `ElasticSearch Head <https://chrome.google.com/webstore/detail/elasticsearch-head/ffmkiejjmecolpfloofpjologoblkegm?hl=en-US>`_ to view your instance in a browser at ``localhost:9200``.

For more information, please visit the official `Elasticsearch documentation <https://www.elastic.co/guide/en/elasticsearch/guide/current/running-elasticsearch.html>`_.

.. important::
   1. By default, Elasticsearch uses 2GB of memory (RAM). For basic development purposes, we have found it to run well enough on 1GB. Use ``ES_JAVA_OPTS="-Xms1g -Xmx1g" ./bin/elasticsearch -d`` to set the memory allotment on startup (`read more <https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html>`_). You can use the same command to give **more** memory to Elasticsearch in a production setting.

.. important::
    If you get an empty response from ``curl localhost:9200``, this is likely because Elasticsearch security features are not probably set up, see :ref:`Development Configuration` above.

Using the Kibana Dashboard
==========================

https://github.com/archesproject/arches-docs/issues/217

Reindexing The Database
=======================

You may need to reindex the entire database now and then. This can be helpful if a bulk load
failed halfway through, or if you need to point your database at a different Elasticsearch installation.

Be warned that this process can take a long time if you have a lot of resources in your database.
Also, if you are in ``DEBUG`` mode it can cause your server to run out of memory.

See :ref:`reindex the database` for the commands needed for reindexing.

Using Multiple Nodes
====================

In production it's advisable to have multiple Elasticsearch instances working together as nodes of
a single cluster. To do this, you need to install a second Elasticsearch instance, and change the
``config/elasticsearch.yml`` file in each instance. Note that the cluster and node names can be whatever
you want, as long as the ``cluster.name`` is the same in both instances and the ``node.name`` is unique
to each one.

**Master (Original) Node Config**

.. code:: yaml

    http.port: 9200

    cluster.name: arches-app
    node.name: arches-app-node1

    node.master: true
    node.data: true

**Secondary Node Config**

.. code:: yaml

    http.port: 9201

    cluster.name: arches-app
    node.name: arches-app-node2

    node.master: false
    node.data: true

**Leave all other parameters untouched.**

You'll need to start/stop each of these instances individually, but you should always
have both running. When they are, the secondary node will automatically find the master
node and the indices will be replicated between the two.

Nothing about your project's ``settings.py`` should change; Arches need only connect
to the original Elasticsearch instance as before. However, you'll see now in the console output
that the cluster health will be ``[GREEN]`` when you have two nodes running (it's ``[YELLOW]``
if you only have one).

.. seealso::

    Here's some `background <http://chrissimpson.co.uk/elasticsearch-yellow-cluster-status-explained.html>`_
    and a `stack overflow question <https://stackoverflow.com/questions/35717790/how-to-add-a-new-node-to-my-elasticsearch-cluster>`_
    with instructions for adding a node.


Adding a Custom Index
=====================

Arches allows you to create a custom index of resource data for your specific use case (for use in Kibana for example).

To add a new custom index create a new python module and add to it a class that inherits from **arches.app.search.base_index.BaseIndex** and implements the **prepare_index** and **get_documents_to_index** methods.

Example custom index:

.. code:: python

    from arches.app.search.base_index import BaseIndex

    class SampleIndex(BaseIndex):
        def prepare_index(self):
            self.index_metadata = {"mappings": {"_doc": {"properties": {"tile_count": {"type": "keyword"}, "graph_id": {"type": "keyword"}}}}}
            super(SampleIndex, self).prepare_index()

        def get_documents_to_index(self, resourceinstance, tiles):
            return ({"tile_count": len(tiles), "graph_id": resourceinstance.graph_id}, str(resourceinstance.resourceinstanceid))

add this to your settings_local.py file

.. code:: python

    ELASTICSEARCH_CUSTOM_INDEXES = [{
        'module': '{path to file with SampleIndex class}.SampleIndex',
        'name': 'my_new_custom_index' <-- follow ES index naming rules, use this name to register in Elasticsearch
    }]

Register your index in Elasticsearch: see :ref:`register a custom index`
