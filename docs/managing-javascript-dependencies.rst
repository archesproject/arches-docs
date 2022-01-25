################################
Managing JavaScript Dependencies
################################

The only dependency in a new project's ``package.json`` file is Arches itself:

.. code-block:: json

    {
        "name": "my_project",
        "dependencies": {
            "arches": "archesproject/arches#stable/6.0.1"
        }
    }

This means that when you run ``yarn install`` on this file, all dependencies from the corresponding branch of the core Arches repo will be installed (in this example, `package.json from stable/6.0.1 <https://github.com/archesproject/arches/blob/stable/6.0.1/package.json>`_).

If you are creating a custom component that requires a new JS package, you will just need to run ``yarn add <package name>`` in your project. This will install the new package and update your ``package.json`` accordingly.

For example, to add `OpenLayers <https://openlayers.org>`_, use ``yarn add ol``. Your ``package.json`` will now look something like:

.. code-block:: json

    {
        "name": "my_project",
        "dependencies": {
            "arches": "archesproject/arches#stable/6.0.1",
            "ol": "^6.12.0"
        }
    }

If you are developing a project, keep track of which version of Arches you are developing against and make sure it is properly reflected in your ``package.json``.

.. note::

    When you register a custom extension through the command line (or load a package with one in it) there is no way to automatically install a new JS dependency, so you'll need to manually run ``yarn add`` as described above.
