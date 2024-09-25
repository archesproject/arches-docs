######################
Installing Core Arches
######################

Most of the instructions here will focus on installation of Arches on the Ubuntu distribution of Linux. Arches can also be installed on Windows and macOS, but installation on those operating systems will likely require additional configuration and debugging. 

.. seealso::

    If you plan to extend or contribute to Arches, please see :ref:`Creating a Development Environment`.

.. seealso::

    We have an in-progress `Docker install <https://github.com/archesproject/arches/tree/master/docker>`_, and would love help improving it. You can also review some works-in-progress and community-created approaches to using Docker :ref:`Installation with Docker`


Installation on Windows via WSL
-------------------------------
Some of the directions below will provide some guidance to instal Arches dependencies and core Arches on machines running the Windows operating system. However, installation on Windows will likely require more configuration (and troubleshooting) than installation on a Linux distribution like Ubuntu. Fortunately, the Windows operating system has a feature called `"Windows Subystem for Linux" (WLS) <https://learn.microsoft.com/en-us/windows/wsl/about>`_ that allows one to run a Linux environment on a Windows machine. With WSL, one can install Arches dependencies and core Arches on an Ubuntu (or other Linux distribution) virtual machine. The steps for installing Arches on a WSL Ubuntu virtual machine will be identical to the steps used to install Arches on an "bare-metal" Ubuntu machine. 

Currently, WSL comes in two architectures. We recommnd using the current default "WSL 2" version of WSL because it has a better file system performance and other benefits. It should be simpler and easier to install Arches on Windows machines via WSL (especially WSL 2). 



Create a Virtual Environment
----------------------------

.. sidebar:: Virtual Environment Reference

    If you are unfamiliar with virtual environments, please take a look at the `Python documentation <https://docs.python.org/3.10/tutorial/venv.html>`_ before continuing.

You need a **Python 3.10+** virtual environment. :ref:`Skip ahead <Install Arches with pip>` if you have already created and activated one. Otherwise, use the commands below for a quick start.

**Create a virtual environment**::

    python3 -m venv ENV

This will generate a new directory called ``ENV``.

.. note::

  On some linux distributions, if the python version is less than 3.10, entering the following command may yield an error but it should alert you to any dependencies you may need to install, after which you'll be able to run this command.

**Activate the virtual environment**

The following are relative paths to an ``activate`` script within ENV.

*Linux and macOS*::

    source ENV/bin/activate

*Windows*::

    ENV\Scripts\activate.bat

.. note::

  After you activate your virtual environment, your command prompt will be prefixed with ``(ENV)``. From here on the documentation will assume you have your virtual environment activated. Run ``deactivate`` if you need to deactivate the virtual environment.

**Test the Python version in ENV**::

    python

This will run the Python interpreter and tell you what version is in use. If you don't
see at least 3.10, check your original Python installation, delete the entire ``ENV``
directory, and create a new virtual environment. Use ``exit()`` or ``ctrl+C`` to
leave the interpreter.

**Upgrade pip**

A recommended step, though not always strictly necessary::

    python -m pip install --upgrade pip

Install Arches with pip
------------------------

Use the following to get the latest stable release of Arches::

    pip install arches

:ref:`Common Errors`

#############################
Creating a New Arches Project
#############################

A Project holds branding and customizations that make one installation of Arches different from the next. The name of your project must be **lowercase** and use **underscores** instead of spaces or hyphens. The example below uses ``my_project``.

Create a Project
----------------

*Linux and macOS*::

    arches-admin startproject my_project

*Windows*::

    python ENV\Scripts\arches-admin startproject my_project

:ref:`Common Errors`

.. note::

    You can add ``--directory path/to/dir`` to change the directory your new project will be created in.


.. warning::

    On Windows, open ``my_project\my_project\settings_local.py`` and add the following line::

        GDAL_LIBRARY_PATH = "C:/OSGeo4W64/bin/gdal201.dll"

    Be sure to adjust the path as necessary for your GDAL installation, and note the *forward* slashes.


.. warning::

    On macOS, ``pip install`` will often fail because the installation of ``psycopg`` (a Postgres driver for Python) needs to access Postgres' ``pg_config`` and does so by looking in the ``PATH``. Some methods for installing Postgres on macOS will require one to manually edit their user profile to edit their profile configuration file e.g. ``.zprofile`` or ``.zshrc`` (`see background <https://www.freecodecamp.org/news/how-do-zsh-configuration-files-work/>`_). You'll need to create or update your user's ``.zshrc`` as so:

    .. code-block:: bash

        # Use a text editor to create or modify your user's .zshrc file
        nano ~/.zshrc

        # Add this line to the .zshrc file, then save the update.
        export PATH="/Applications/Postgres.app/Contents/Versions/14/bin:$PATH"

        # Make sure the update to the .zshrc file takes effect
        source ~/.zshrc

    In addition, a macOS installation will likely require some modifications to ``settings.py`` (or ``settings_local.py``) in your project directory to specify GDAL and GEOS related paths. (See :ref:`macOS and GDAL, GEOS`)


Setup the Database
-------------------

First, enter the project directory::

    cd my_project

and then run::

    python manage.py setup_db

.. note:: You may be prompted to enter a password for the ``postgres`` user. Generally, our installation scripts set this password to ``postgis``, however you may have set a different password during your own Postgres/PostGIS installation.

:ref:`Common Errors`

Build a Frontend Asset Bundle
-----------------------------

In your current terminal, run the Django development server (with the Arches virtual environment activated)::

    python manage.py runserver

Then, in a second terminal, activate the virtual environment used by Arches (this is a required step). Then navigate to the root directory of the project. ( you should be on the same level as `package.json`) and build a frontend asset bundle::

    cd my_project/my_project
    npm run build_development

If you have trouble with this step, see :ref:`Troubleshooting Frontend Builds` below.

.. note::

    ``npm run build_development`` creates a static frontend asset bundle. Any changes made to frontend files (eg. ``.js``) will not be viewable until the asset bundle is rebuilt. run ``npm run build_development`` again to update the asset bundle, or run ``npm start`` to run an asset bundler server that will detect changes to frontend files and rebuild the bundle appropriately.






View the Project in a Browser
-----------------------------

Navigate to ``localhost:8000`` in a browser. Use ``ctrl+C`` to stop the server.

Configure the Map Settings
--------------------------

The first thing everyone wants to do is look at the map, so let's set this up first.

1. Go to Mapbox.com and create a free account.
2. Find your default API key (starts with ``pk.``) and copy it.
3. Now go to ``localhost:8000/settings``.
4. Login with the default credentials: **username**: ``admin`` **password**: ``admin``
5. Find the **Default Map Settings**, and enter your *Mapbox API* Key there.
6. Feel free to use the ``?`` in the top-right corner of the page to learn about all of the other settings, and change any that you like (heed warning below).
7. Save the settings.
8. Navigate to ``localhost:8000/search`` to make sure the basemap appears.

.. note::

    We recommend exporting these settings by running ``python manage.py packages -o save_system_settings``.
    This will create a JSON file in your project, which will be used if you ever need
    to setup your database again.

.. warning::

    If you create a new **Project Extent**, you should also update the **Search Results Grid** settings,
    otherwise you could get a JSON error in the search page. To be on the safe side, choose
    a high *Hexagon Size* combined with a low *Hexagon Grid Precision*.

Load a Package
--------------

An Arches "package" is an external container for database definitions (graphs, concept schemes),
custom extensions (including functions, widgets, datatypes) and even data (resources).
Packages are installed into projects, and can be used to share schema between installations.

To get started, load this sample package::

    python manage.py packages -o load_package -s https://github.com/archesproject/arches-example-pkg/archive/master.zip -db

Go to ``localhost:8000/graph`` to see 6 Resource Models that you can now use. You can also create new Resource models from scratch.

Go to ``localhost:8000/resource`` to begin creating resources based on one of these resource models.

Go to ``localhost:8000/search`` to find and inspect resources that you have created.

You can add ``-dev`` to the load_package command to create a few test user accounts.

What Next?
----------

* Read more about :ref:`Projects and Packages <Understanding Projects>`

Common Errors
-------------

* On macOS, If you get this error

    .. error:: `ValueError: --enable-zlib requested but zlib not found, aborting.`

    try running ``xcode-select --install`` (`reference <http://stackoverflow.com/questions/32909426/zlib-error-when-installing-pillow-on-mac>`_)

* Getting a connection error like this (in the dev server output or in the browser)

    .. error:: `ConnectionError: ConnectionError(<urllib3.connection.HTTPConnection object at 0x0000000005C6BC50>: Failed to establish a new connection: [Errno 10061] No connection could be made because the target machine actively refused it) caused by: NewConnectionError(<urllib3.connection.HTTPConnection object at 0x0000000005C6BC50>: Failed to establish a new connection: [Errno 10061] No connection could be made because the target machine actively refused it)`

    means Arches is not able to communicate with ElasticSearch. Most likely, ElasticSearch is just not running, so just start it up and reload the page. If you can confirm that it `is` running, make sure Arches is pointed to to correct port.

* Postgres password authentication error

    .. error:: `django.db.utils.OperationalError: FATAL: pw authentification  failed for user postgres`

    Most likely you have not correctly set the database credentials in your ``settings.py`` file. Many of our install scripts set the db user to ``postgres`` and password to ``postgis``, so that's what Arches looks for by default. However, if you have changed these values (particularly if you are on Windows and had to enter a password during the Postgres/PostGIS installation process), the new values must be reflected in in ``settings.py`` or ``settings_local.py``.

    .. note::

        On Windows, you can avoid having to repeatedly enter the password while running commands in the console by setting the PGPASSWORD environment variable: ``set PGPASSWORD=<your password>``.


Troubleshooting Frontend Builds
-------------------------------

Building the frontend assets can sometimes be a source of challenge and frustration. Sometimes a "locked down" computer (with strict security configurations) may cause some trouble. If this is the case, you can try the following steps to interate toward a successful build.

1. Configure ``npm`` to disable strict SSL.
    .. code-block:: bash

        npm config set cafile null
        npm config set strict-ssl false

2. Remove the ``node_modules`` folder and ``package-lock.json`` file if they exist:
    .. code-block:: bash

        cd path/to/dir/my_project/my_project
        rm -rf node_modules
        rm package-lock.json

3. If you’re using a virtual environment, activate it. ENV should be replaced with the name of your virtual environment.
    .. code-block:: bash

        source ENV/bin/activate

4. Run your Arches Django server and leave it running.
    .. code-block:: bash

        python manage.py runserver

5. **Open a *new terminal* to complete the following steps below.**

6. If you’re using a virtual environment, activate it as in step 4 above. ENV should be replaced with the name of your virtual environment.
    .. code-block:: bash

        source ENV/bin/activate

7. Navigate to the same directory as package.json, and install the frontend dependencies:
    .. code-block:: bash

        cd path/to/dir/my_project/my_project
        npm install

8. Once the dependencies are installed, build your static asset bundle:
    .. code-block:: bash

        npm run build_development


    If successful, you should see a message indicating that the build was successful. A successful build should make a message looking something like this:

        cacheable modules 8.62 MiB (javascript) 3.28 KiB (asset)
        modules by path ./media/ 6.48 MiB 996 modules
        modules by path ../../ 2.15 MiB (javascript) 3.28 KiB (asset)
        modules by path ../../arches/arches/app/media/ 1.2 MiB (javascript) 3.28 KiB (asset) 264 modules
        modules by path ../../arches/arches/app/templates/views/ 970 KiB 90 modules
        ../../arches-rdm/arches_rdm/media/js/.gitkeep 1 bytes [built] [code generated]
        ./media/js/ sync ^\.\/.*$ 207 bytes [optional] [built] [code generated]
        ../../arches/arches/app/media/js/ sync ^\.\/.*$ 18.9 KiB [optional] [built] [code generated]
        ../../ENV/lib/python3.10/site-packages/ sync ^\.\/.*\/media\/js\/.*$ 160 bytes [optional] [built] [code generated]
        ../../arches-rdm/arches_rdm/media/js/ sync ^\.\/.*$ 160 bytes [optional] [built] [code generated]
        ../../arches/arches/app/media/js/utils/ sync ^.*\/media\/js\/.*$ 160 bytes [optional] [built] [code generated]
        ./media/node_modules/moment/locale/ sync ^\.\/.*$ 3.21 KiB [optional] [built] [code generated]
        webpack 5.89.0 compiled successfully in 8545 ms
        ✨  Done in 10.71s.
