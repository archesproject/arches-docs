#########################
Requirements/Dependencies
#########################

System Requirements
===================

Arches works on Linux, Windows, or macOS. Most production implementations use Linux servers.

To begin development or make a test installation of Arches, you will need the following **minimum** resources:

:Disk Space: - **2GB** for all dependencies and Arches.
    - **8GB** to store uploaded files, database backups, etc.
    - Depending on how many uploaded files (images, 3d models, etc) you will have, you may need **much** more disk space. We advise an early evaulation of how much space you *think* you'll need, and then provision twice as much just to be safe...
:Memory (RAM):  - **4GB**
    - This recommendation is based on the fact that ElasticSearch requires 2GB to run, and as per `official ElasticSearch documentation <https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html#_give_less_than_half_your_memory_to_lucene>`_ no more than half of your system's memory should be dedicated to ElasticSearch.
    - In production, you very likely need to increase your memory. In building the production (minified) frontend asset bundle, yarn (all by itself!) will require at least 8GB to run. If you don't have enough memory, yarn will likely return an error, sometimes after several minutes or hours of processing. In production, you may also find it useful to allow ElasticSearch to use `up to 32GB <https://www.elastic.co/guide/en/elasticsearch/guide/current/heap-sizing.html#compressed_oops>`_.


Software Dependencies
=====================

Arches requires the following software packages to be installed and available. Ubuntu Linux users see below for an installation script.

:Python >= 3.10: - Installation: https://www.python.org/downloads/
    - Python 3.10 and later comes with pip
    - **Windows** You must choose 32-bit or 64-bit Python based on your system architecture.
    - **macOS** This guide works well if you wish to install via `brew`: https://docs.python-guide.org/starting/install3/osx/
:Git >= 2.0: - Installation: https://git-scm.com/downloads
    - **Windows** Choose the "Use Git from the Windows Command Prompt" option during installation.
    - **macOS** You can install Git via `brew`: https://brew.sh/
:PostgreSQL >= 12 with PostGIS 3:
    - **macOS** Use `Postgres.app <http://postgresapp.com>`_.
    - **Windows** Use the `EnterpriseDB installers <https://www.postgresql.org/download/windows/>`_, and use Stack Builder (included) to get PostGIS. After installation, add the following to your system's ``PATH`` environment variable: ``C:\Program Files\PostgreSQL\12\bin``. Make sure you write down the password that you assign to the ``postgres`` user.
:Elasticsearch 8: - Installers: https://www.elastic.co/downloads/past-releases/elasticsearch-8-5-1
    - Elasticsearch is integral to Arches and can be installed and configured many ways.
      For more information, see :ref:`Arches and Elasticsearch`.
:GDAL >= 2.2.x: 
    - **Windows** Use the `OSGeo4W installer <https://trac.osgeo.org/osgeo4w/>`_, and choose to install the GDAL package (you don't need QGIS or GRASS). After installation, add ``C:\OSGeo4W64\bin`` to your system's ``PATH`` environment variable.
    - **macOS** (See :ref:`macOS and GDAL, GEOS` below)
:Node.js 16.x (recommended): - Installation: https://nodejs.org/ (choose the installer appropriate to your operating system).
    - NOTE: Arches may not be compatible with later versions of Node.js (after 16) `(see discussion) <https://community.archesproject.org/t/newbie-v7-install-experience-some-hints-and-tips/1782>`_.
:Yarn >= 1.22, < 2: - Recommended Installation: https://classic.yarnpkg.com/en/docs/install (One can also install Yarn via `apt` on Linux operating systems, `see example <https://github.com/archesproject/arches/blob/f06b838cf1be23471644f8528a630d65c8bff9a7/arches/install/ubuntu_setup.sh#L51>`_).
    - NOTE: We are pointing to the "classic" yarn installer to avoid installation of more recent versions of yarn that are not compatible with Arches via the Node.js `package manager <https://yarnpkg.com/getting-started/install>`_.

To support long-running task management, like large user downloads, you must install a Celery broker like RabbitMQ or Redis:

:Brokers: - Options: https://docs.celeryproject.org/en/stable/getting-started/first-steps-with-celery.html#choosing-a-broker
    - Once you have a broker installed, read more about :ref:`Task Management` in Arches.


macOS and GDAL, GEOS
--------------------
Satisfying GDAL and GEOS requirements for **macOS** installations can involve some additional complexity, especially if using the Apple M1 series of ARM-based system-on-a-chip (SoC) hardware. You'll need to install GDAL and GEOS in preparation for installing Python libraries that need this requirement. To install GDAL and GEOS:

.. code-block:: bash

    brew install gdal 
    brew install geos

Currently, GDAL version 3.8 and GEOS version 3.12 work with Arches running on macOS. Once you've completed installation of dependencies and have created an Arches project (see :ref:`Create a Project`), you will likely need to specify the paths to the GDAL and GEOS libraries in your ``settings.py`` file. Here is an example of what to add to ``settings.py`` in a macOS installation:

.. code-block:: python

    GDAL_LIBRARY_PATH = '/opt/homebrew/Cellar/gdal/3.8.4_3/lib/libgdal.34.3.8.4.dylib'
    GEOS_LIBRARY_PATH = '/opt/homebrew/Cellar/geos/3.12.1/lib/libgeos_c.dylib'




Scripted Dependency Installation
--------------------------------

For Ubuntu we maintain an `ubuntu_setup.sh <https://raw.githubusercontent.com/archesproject/arches/stable/7.5.0/arches/install/ubuntu_setup.sh>`_ script to install dependencies. It works for 18.04 and 20.04, and preliminary testing shows it to be compatible with 22.04 as well.

.. code-block:: bash

    wget https://raw.githubusercontent.com/archesproject/arches/stable/7.5.0/arches/install/ubuntu_setup.sh
    source ./ubuntu_setup.sh

You will be prompted before each dependency is installed, or use ``yes | source ./ubuntu_setup.sh`` to install all components (Postgres/PostGIS, Node/Yarn, and ElasticSearch).