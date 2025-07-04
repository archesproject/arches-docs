######################
Command Line Reference
######################

+ `Installation Commands`_
+ `ElasticSearch Management`_
+ `Import Commands`_
+ `Export Commands`_
+ `Managing Functions, DataTypes, Widgets, and Card Components`_
+ `Other Useful Django Commands`_

This page serves as a quick reference guide for working with Arches
through a command prompt. Along with default Django commands, a good
deal of Arches operations have been added to ``manage.py``. In a
command prompt, [activate your virtual
environment](Dev-Installation#4-activate-the-virtual-environment),
then run the following commands from your root app directory (the one
that contains ``manage.py``).

_All file or directory path parameters (``-s``, ``-c``, ``-d``) should
be absolute paths._

Installation Commands
=====================

installing from a local repo clone
----------------------------------

.. code-block:: shell

    pip install -e .

-e      This argument with the value ``.`` indicates to pip that it should link the local directory with the virtual environment.

Installs Arches into your virtual environment from a local clone of
the `archesproject/arches <https://github.com/archesproject/arches>`_
repo, or your own fork of that repo. To do this properly, create a new
virtual environment and activate it, clone the repo you want, enter
that repo's root directory, and then run the command.

If you wish to install the development dependencies too, run `pip install -e '.[dev]'` instead.


creating an Arches project
--------------------------

.. code-block:: bash

   arches-admin startproject <name_of_project> [{-d|--directory} <directory_name>]

-d, --directory
    (Optional) The name of the directory you'd like your new project located in.
    
    If `-d` is not specified, the new project will be created in the current working directory
    with the name of the project. To match python package `naming conventions
    <https://peps.python.org/pep-0008/#package-and-module-names>`_,
    underscores (`_`) will be replaced with dashes (`-`) in that directory name, 
    which is important if you plan on publishing your project to PyPi as an 
    :ref:`Arches Application<Creating Applications>`.



creating (or recreating) the database
-------------------------------------

.. code-block:: bash

    python manage.py setup_db

Deletes and recreates the database, as defined by
``settings.DATABASES['default']``. Likewise, **this command will
remove all existing data**.

loading a package into a project
--------------------------------

.. code-block:: bash

    python manage.py packages -o load_package -s source_of_package [-db]

-db
        Add this boolean argument to force the destruction
        and recreation of your database before loading the package.

The source (``-s``) of a package can be either a path to a local
directory, the location of a local zipfile containing a package, or
the url to a github repo archive that contains a package. For example,
loading the sample package from where it resides in github would
just be::

    python manage.py packages -o load_package -s https://github.com/archesproject/arches-example-pkg/archive/master.zip

ElasticSearch Management
========================

reindex the database
--------------------

Note that commands using ``python manage.py es [command]`` require ElasticSearch to be running.

.. code-block:: bash

    python manage.py es reindex_database

This single command wraps the three following commands (each of which can be run individually if desired).

.. code-block:: bash

    python manage.py es delete_indexes
    python manage.py es setup_indexes
    python manage.py es index_database

.. important::
    If ``DEBUG = True``, memory usage will continuously increase during indexing, because Django stores
    all db queries in memory, and a lot of them happen during indexing. Be wary of this during development
    when indexing large databases, or on servers with small memory provisions (you may want to temporarily
    set ``DEBUG = False``).

Starting with version 7.4, you can add the ``-rd`` or ``--recalculate-descriptors`` flag to the reindex management command to force resource instance primary descriptors to be recalculated prior to reindexing. See below:

.. code-block:: bash

    python manage.py es reindex_database --recalculate-descriptors

register a custom index
-----------------------

.. code-block:: bash

    python manage.py es add_index --name {index name}

See :ref:`Adding a Custom Index`

Import Commands
===============

Import Resource Models or Branches in archesjson format
-------------------------------------------------------
.. code-block:: bash

   python manage.py packages -o import_graphs [-s path_to_json_directory_or_file]

-s
        Path to the source file you are importing. If not specified, the
        command will look to ``settings.RESOURCE_GRAPH_LOCATIONS`` for
        directory paths

Import reference data in skos/rdf format
----------------------------------------

.. code-block:: bash

   python manage.py packages -o import_reference_data -s 'path_to_rdf_file' [-ow {'overwrite'|'ignore'}] [-st {'stage'|'keep'}]

Import business data
--------------------
.. code-block:: bash

   python manage.py packages -o import_business_data -s 'path_to_source_file' [-c 'path_to_mapping_file'] [-ow '{overwrite'|'append'}] [--create_concepts {'create'|'append'}] [--bulk_load]

-c
        The path to the mapping file. The mapping file tells Arches how to
        map the columns from your csv file to the nodes in your
        resource graph. This option is required if there is not a
        mapping file named the same as the business data file and in
        the same directory with extension '.mapping' instead of '.csv'
        or '.json'.
-ow
        Determines how resources with duplicate ResourceIDs will be
        handled: ``append`` adds more tile data to an existing
        resource; ``overwrite`` replaces any existing resource with
        the imported data. This option only applies to CSV
        import. **JSON import always overwrites**.
-bulk, --bulk_load
       Bulk load values into the database. By setting this flag the
       system will use Django's `bulk_create
       <https://docs.djangoproject.com/en/dev/ref/models/querysets/#bulk-create>`_
       operation. The model's ``save()`` method will not be called,
       and the ``pre_save`` and ``post_save`` signals will not be
       sent.
--create_concepts
        Creates or appends concepts and collections to your rdm
        according to the option you select. ``create`` will create
        concepts and collections and associate them to the mapped
        nodes. ``append`` will append concepts to the existing
        collections assigned to the mapped nodes and create
        collections for nodes that do not have an assigned collection.


.. seealso:: See :ref:`CSV Import` for CSV formatting requirements.

Import resource to resource relations
-------------------------------------
.. code-block:: bash

    python manage.py packages -o import_business_data_relations -s 'path_to_relations_file'


See :ref:`Importing Resource Relations`

Export Commands
===============

export branch or resource model schema
--------------------------------------

.. code-block:: bash

    python manage.py packages -o export_graphs -d 'path_to_destination_directory' -g uuid/branches/resource_models/all

-o          ``packages`` operation, in this case ``export_graphs``
-d          Absolute path to destination directory
-g
        UUID of specific graph, or ``branches`` for all branches,
        ``resource_models`` for all resource models, or ``all`` for
        everything.

Exports Resource Models and/or Branches. Note that sometimes (as in
this case) Resource Models and Branches are generically called
"graphs".

export business data to csv or json
-----------------------------------

.. code-block:: bash

    python manage.py packages -o export_business_data -d 'path_to_destination_directory' -f 'csv' or 'json' [-c 'path_to_mapping_file' -g 'resource_model_uuid' -single_file]

-o
        `packages` operation, in this case ``export_business_data``
-d
        Absolute path to destination directory
-f
        Export format, must be ``csv`` or ``json``
-c
        (required for csv) Absolute path to the mapping file you would
        like to use for your csv export.
-single_file
        (optional for csv) Use this parameter if you'd like to export
        your grouped data to the same csv file as the rest of your
        data.
-g
        (required for json, optional for csv) The resource model UUID
        whose instances you would like to export.

Exports business data to csv or json depending on the -f parameter
specified. For csv export a mapping file is required. The exporter
will export all resources of the type indicated in the
resource_model_id property of the mapping file and the -g parameter
will be ignored. For json export no mapping file is required, instead
a resource model uuid should be passed into the -g command.

Outputs a csv file with the business data for each resource. For nodes with data from multiple tiles, the command splits the additional data into overall several lines, which are then saved in a separate csv file ending ‘_grouped’. If the --single_file option is used, then the additional rows are included in the main csv file instead. Finally, a relations file is produced that includes all relationships between resources. 

Note that in a Windows command prompt, you may need to replace ``'`` with ``"``.

export business data to shapefile
---------------------------------

.. code-block:: bash

    python manage.py export shp -t 'name_of_db_view' -d 'output_directory'

-t
        A resource instance database view
-d
        The destination directory for point, line, and polygon
        shapefiles, created when the command is run.

business data export examples
-----------------------------

.. code-block:: bash

    python manage.py packages -o export_business_data -f 'csv' -c 'path_to_mapping_file'

Exports all business data of the resource model indicated in the
mapping file. Two files are created. The first file contains one row
per resource (if you resources all have the same geometry type this
file can be used to create a shape file in QGIS or other program). The
second file contains the grouped attributes of your resources (for
instance, alternate names, additional classifications, etc.).

.. code-block:: bash

    python manage.py packages -o export_business_data -f 'json' -g 'resource_model_id'

-f  'json' or 'csv'

Exports all business data of the passed in resource_model_id to the
specified file format. Take a look at the ``RESOURCE_FORMATERS``
dictionary in Arches' ``settings.py`` for some other interesting
options.

Other Data Management Commands
==============================

remove resources
----------------
.. code-block:: bash

    python manage.py resources remove_resources [-g graph_id][-y][-e]

-g  A Graph UUID to remove all the resource instances of.
-y  Forces this command to run without interactive confirmation.
-e  Removes all records from the edit log for the resources that are removed. If a graphid is provided, only the edit log records for that graph will be removed.

Removes all resources from your database, but leaves the all resources
models, branches, thesauri, and collections intact.

purge edit log
--------------
.. code-block:: bash

    python manage.py resources clear_edit_log [-g graph_id]

-g  A Graph UUID to filter which edit log entries are removed.

Removes all entries from the Arches Edit Log.

create mapping files
--------------------
.. code-block:: bash

    python manage.py packages -o create_mapping_file -d 'path_to_destination_directory' -g 'comma separated graph uuids'

-d  Path to directory to place the output in.
-g  The graph UUID for which to create a mapping.

This mimics the 'Create Mapping File' command from the Arches Designer UI. See also :ref:`Mapping File` background.

import mapping file
-------------------
.. code-block:: bash

    python manage.py packages -o import_mapping_file -s 'path_to_mapping_file'


Imports a mapping file for a particular resource model. This will be
used as the export mapping file for a resource by default (e.g. for
search export).


Ontology Commands
=================

load an ontology
----------------

.. code-block:: bash

    python manage.py load_ontology [-s <path to ontology directory>]

-s
        Path to new ontology directory to load


Managing Functions, DataTypes, Widgets, and Card Components
===========================================================

To learn how to build new Functions, DataTypes, Card Components, or Widgets,
please see :ref:`Functions`, :ref:`Widgets`, :ref:`Card Components`, or
:ref:`Datatypes`.
**Note that when importing Widgets and associated DataTypes, Widgets
must be registered first.**

function commands
-----------------

**list registered functions**

.. code-block:: bash

    python manage.py fn list

Lists all currently registered functions.

**registering functions**

.. code-block:: bash

    python manage.py fn register --source path/to/your/function.py

Register a newly created function. These ``.py`` files should sit in
your projects ``functions`` directory.

**unregistering functions**

.. code-block:: bash

    python manage.py fn unregister -n 'Sample Function'

Unregister a function. Use the function name that is returned by ``fn
list``.

datatype commands
-----------------

**list registered datatypes**

.. code-block:: bash

    python manage.py datatype list

Lists all currently registered datatypes.

**registering and updating datatypes**

.. code-block:: bash

    python manage.py datatype register --source /Users/me/Documents/projects/mynewproject/mynewproject/datatypes/wkt_point.py

Registers a new datatype, in this example as defined in ``wkt_point.py``.

.. code-block:: bash

    python manage.py datatype update --source /Users/me/Documents/projects/mynewproject/mynewproject/datatypes/wkt_point.py

Updates a datatype, necessary anytime changes are made to your
datatype's properties.

-source Location of the ``.py`` file that defines the datatype.


**unregister a datatype**

.. code-block:: bash

    python manage.py datatype unregister -d 'wkt-point'

Unregisters a datatype, in this example a datatype named
``wkt-point``.

-d  Name of datatype to unregister. Use the datatype name that is returned by ``datatype list``.

widget commands
---------------

All widget-related commands are identical to those for datatypes, just
substitute ``widget`` for ``datatype``. Also note that where datatypes
are defined in ``.py`` files, widgets are defined in ``.json`` files.


card component commands
-----------------------

All component-related commands are identical to those for widgets,
just substitute ``card_component`` for ``widget``. JSON files are used
to register Card Components.


Creating and Deleting Map Layers
================================


See :ref:`Creating New Map Layers` for file format requirements and other in-depth information.

Add a MapBox Layer
------------------
.. code-block:: bash

   python manage.py packages -o add_mapbox_layer -j /path/to/mapbox_style.json -n "New MapBox Layer" [{-b|--is_basemap}] [{-i|--layer_icon} 'icon_class'}]

-j  The path to the Mapbox JSON file
-n  The name of the Mapbox layer


Delete a MapBox Layer
---------------------
.. code-block:: bash

   python manage.py packages -o delete_mapbox_layer -n "name of map layer to be deleted"

-n  The name of the Mapbox layer



Other Useful Django Commands
============================

Run the django webserver
------------------------

.. code-block:: bash

    python manage.py runserver

Run the Django dev server. Add ``0.0.0.0:8000`` to explicitly set the
host and port, which may be necessary when using remote servers, like
an AWS EC2 instance. More about `runserver
<https://docs.djangoproject.com/en/stable/ref/django-admin/#runserver>`_.

collect static files
--------------------

.. code-block:: bash

    python manage.py collectstatic

Collects all static files and places them in a single
directory. Generally only necessary in production. Also allows all
static files to be `hosted on another server
<https://docs.djangoproject.com/en/stable/howto/static-files/deployment/#serving-static-files-from-a-cloud-service-or-cdn>`_).

Django's full ``manage.py`` commands are documented `here
<https://docs.djangoproject.com/en/stable/ref/django-admin/#available-commands>`_.
