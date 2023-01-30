######################
Migrating Data from v3
######################

.. sidebar:: Terminology Note

    In v3 we had "resource graphs", while in v4 and later we call these "Resource Models". Conceptually they are the same. We'll be referring to them here as "v3 graphs" and "Resource Models", respectively.

.. note:: In the following guides, you'll see mention of "v4". However, all of these steps work for Arches v5, as well.

Upgrading your Arches installation is a complex process, as a significant backend redesign was implemented in v4. We have developed the following documentation (and the code to support it) to guide you through the process. You will be performing a combination of shell commands and basic file manipulation.

Before migrating data, you'll need to :ref:`install core Arches <Installing Core Arches>` and :ref:`create a new project <Creating a new Arches Project>`. You can name your project whatever you want, but throughout this documentation we'll refer to it as ``my_project``. You can customize the templates and images in your project any time (before or after migrating the data). We recommend adding a Mapbox key right away so you can use the map for visual checks during the migration.

.. seealso::

    Please see the main :doc:`installation guide </installing/installation>`.

Before moving on, you must be able to run the Django development and view your project in a browser at ``http://localhost:8000``.

Once you are ready, you can begin the migration process. The overall form of the process goes like this:

+ Export data from existing v3 Arches installation
+ Create a package (Arches-HIP users: this is already done for you)
+ Place the v3 data into the Package directories
+ Run commands to convert the v3 data to v4 data
+ Load the package into any v4 project

---------------------------
Exporting Your Data From v3
---------------------------

You must export all of your data from v3. Before you begin, however, you'll need to install some enhanced commands into your v3 app. This is a simple process:

#. Download and unzip `arches3-export-utils-master.zip <https://github.com/legiongis/arches3-export-utils/archive/master.zip>`_ (`source <https://github.com/legiongis/arches3-export-utils>`_)
#. Copy the "management" directory into your v3 app alongside the ``settings.py`` file.
#. In your v3 environment, run ``python manage.py v3v4 --help`` to make sure the new commands have been been installed.

.. warning::
    Be sure to backup your v3 database before beginning the export process.

Now you are ready to begin exporting your data from v3. Follow these steps:

.. toctree::
    :maxdepth: 2

    exporting-v3-data

After you have all the v3 data exported, you are ready to follow the appropriate workflow for your deployment.

-------------------
Migrating Your Data
-------------------

The workflow you must use for the migration depends on the nature of your v3 deployment.

Arches-HIP App
--------------

If your v3 deployment of Arches was based on **Arches-HIP**, and you did not modify any of the graphs (beyond perhaps changing node names) you can use the Arches-HIP Workflow. If you have changed the RDM content that's fine, it will be preserved through the migration.

.. toctree::
    :maxdepth: 2

    migrate-hip-app

App With Custom Graphs
----------------------

If you have a v3 deployment with custom resource graphs, you'll need to use the following workflow. Be aware, you'll need to remake your custom resource graphs in v4 (as "Resource Models"). This is listed as Step 6 below.

.. toctree::
    :maxdepth: 2

    migrate-other-app
