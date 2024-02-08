###########
ETL Modules
###########

The ETL Modules allow a developer to define ETL (`extract, transform, load <https://en.wikipedia.org/wiki/Extract,_transform,_load>`_) processes that fit the user's business case.
Arches includes basic ETL modules. The modules can be accessed in the :ref:`Bulk Data Manager <bulk data manager>`,
which currently supports import, export, and edit.
A user can add a custom module, in addition to the modules inlcuded in the Arches.

Creating an ETL Module
======================

A module comprises three separate files, which should be seen as front-end/back-end complements.
On the front-end, you will need a component made from a Django HTML template and JavaScript pair,
which should share the same basename.

In your Project, these files must be placed accordingly:

    ``/my_project/my_project/media/js/views/components/etl_modules/sample-etl-module.js``
    ``/my_project/my_project/templates/views/components/etl_modules/sample-etl-module.htm``

The third file is a Python file which contains a dictionary telling Arches some important details
about your module, as well as its main logic.

    ``/my_project/my_project/etl_modules/sample_etl_module.py``


Defining the Details
====================

The first step in creating a ETL Module is defining the ``details``
in the top of your Function’s ``.py`` file.
The ``details`` is also used to register you etl module during the package loading or :ref:`on the command line <registering your etl module>`.

.. code-block:: python

    details = {
        "etlmoduleid": "",
        "name": "Sample ETL Module",
        "description": "This module is a sample module",
        "etl_type": "import",
        "component": "views/components/etl_modules/sample-etl-module",
        "componentname": "sample-etl-module",
        "modulename": "sample_etl_module.py",
        "classname": "SampleEtlModule",
        "config": {"bgColor": "#f5c60a", "circleColor": "#f9dd6c"},
        "icon": "fa fa-upload",
        "slug": "sample-etl-module",
        "helpsortorder": 9,
        "helptemplate": "sample-etl-module-help"
    }


:etlmoduleid:
        **Optional** A UUID4 for your ETL Module. Feel free to generate one in advance if that fits your workflow;
        if not, Arches will generate one for you.
:name:
        **Required** The name of your new ETL Module, visible in the icons in the Bulk Data Manager menu.
:description:
        **Required** The description of your new ETL Module, visible in the icons in the Bulk Data Manager menu.
:etl_type:
        **Required** The type of your new ETL Module, currently ``import``, ``export``, and ``edit`` are supported
:component:
        **Required** The path to the component view you have developed.
        Example: ``views/components/etl_modules/sample-etl-module``
:componentname:
        **Required** Set this to the last part of ``component`` above.
:classname:
        **Required** The name of the Python class implementing your ETL Module,
        located in your module's Python file below the details.
:modulename:
        **Required** The name of the Python file implementing your ETL Module.
:config:
        **Required** You can provide user-defined default configuration here.
        Make it a JSON dictionary of keys and values. An empty dictionary is acceptable.
:icon:
        **Required** The icon visible in the icone in the Bulk Data Manager menu.
:slug:
        **Required** The string that will be used in the url to access your ETL Module
:helptemplate:
        **Optional** The help template for your etl module in the Arches help section
:helpsortorder:
        **Optional** The order in which the ETL Module helps will be listed in the Arches help section

The ``config`` field
--------------------

Though not required, typically the ``config`` will include ``bgColor`` and ``circleColor``
that will determine the backgound and the icon colors visible in the ``Bulk Data Manager``.

The additional properties can be added, if you would like to set the default values or add your user-defined configuration.
For example, the string editors have the field ``updateLimit`` (set to 5,000 by default)
which will limit the number of edits in a single etl process.


Writing your ETL Module
=======================

In your module's Python code, you have access to all your server-side models.

The importers and editors follow the pattern of

- creating the intermediary data in ``load_staging`` table as the tile-like json format
- processing the data either before or after staging the data
- validatating the data if necessary (and recording the errors in the ``load_errors`` table)
- saving the data in the ``tile`` table if there are no validation errors
- indexing the database
- The progress needs to be saved in ``load_event`` table, if you want to access the status and the information about the etl.

If you want to take advantage of the pattern, you can start your development by extending
the ``BaseImportModule`` for an importer or ``BaseBulkEditor`` for an editor,
which will provide the basic functionality such as reverse (undo the import or edit).
Then, you may want to write your own functions or overwrite the excisting ones
such as validate, read, preview, or write, as well as run_load_task_async and run_load_task if you would like to utilize the celery task manager.

see the examples in the existing etl module such as base_data_editor.py

.. code-block:: python

    class BulkStringEditor(BaseBulkEditor):
        def validate(self, request):
            ...

        def validate_inputs(self, request):
            ...

        def edit_staged_data(self, cursor, graph_id, node_id, operation, language_code, pattern, new_text):
            ...

        def get_preview_data(self, node_id, search_url, language_code, operation, old_text, case_insensitive, whole_word):
            ...

        def preview(self, request):
            ...

        def write(self, request):
            ...

        @load_data_async
        def run_load_task_async(self, request):
            ...

        def run_load_task(self, userid, loadid, module_id, graph_id, node_id, operation, language_code, pattern, new_text, resourceids):
            ...


Also, you can find the related models in ``models.py`` (``LoadStaging``, ``LoadErrors``, and ``LoadEvent``).


Registering your ETL Module
===========================

To register your ETL Module, use this command:

.. code-block:: bash

    python manage.py etl_module register --source /projects/my_project/my_project/etl_modules/sample_etl_module.py

The command will confirm your ETL Module has been registered, and you can also list the existing modules with:

.. code-block:: bash

    python manage.py etl_module list

To unregister your ETL Module, you can load the changes to Arches with:


.. code-block:: bash

    python manage.py etl_module unregister --name Sample ETL Module


Examples to Get Started with ETL Modules
========================================

As is the case with other custom components in Arches, an html file and a javascript file are needed to design the user interface of your custom component. To help guide development of a custom ETL module, you can look at the files associated with the **Tile Excel Loader** that comes standard with core Arches. These are the component files for that module:

    * `tile-excel-importer.js <https://github.com/archesproject/arches/blob/stable/7.5.1/arches/app/media/js/views/components/etl_modules/tile-excel-importer.js>`_
    * `tile-excel-importer.htm <https://github.com/archesproject/arches/blob/stable/7.5.1/arches/app/templates/views/components/etl_modules/tile-excel-importer.htm>`_

Note that the ``tile-excel-importer.js`` javascript file imports a view model called `excel-file-import.js <https://github.com/archesproject/arches/blob/stable/7.5.1/arches/app/media/js/viewmodels/excel-file-import.js>`_ where most of the logic is located.

You will notice that there are calls to submit that send strings such as "read" and "write" back to the Arches server. These strings are passed back to your module's python file. In other words, calling `await self.submit('start'); <https://github.com/archesproject/arches/blob/stable/7.5.1/arches/app/media/js/viewmodels/excel-file-import.js#L114>`_ will call the corresponding start method in your module.

That flexibility gives you gives one a great deal of freedom to implement custom logic in your ETL module.