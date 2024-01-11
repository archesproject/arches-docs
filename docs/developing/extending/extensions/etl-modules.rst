###########
ETL Modules
###########

The ETL Modules allow a developer to define etl processes that fit the user's business case.
Arches includes basic etl modules. The modules can be accessed in the :ref:`Bulk Data Manager <bulk data manager>`,
which currently supports import, export, and edit.
A user can define custom module, in addition to the modules inlcuded in the Arches.

Registering your ETL Module
===========================

To register your ETL Module, you'll need a JSON configuration ``details``
in the top of your ETL Modeuls's ``.py`` file:

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
        **Required** The name of your new ETL Module, visible in the icons Bulk Data Manager menu.
:description:
        **Required** The description of your new ETL Module, visible in the icons Bulk Data Manager menu.
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

ETL Module Commands
-------------------

To register your ETL Module, use this command:

.. code-block:: bash

    python manage.py etl_module register --source /projects/my_project/my_project/etl_modules/sample_etl_module.py

The command will confirm your ETL Module has been registered, and you can also list the existing modules with:

.. code-block:: bash

    python manage.py etl_module list

To unregister your ETL Module, you can load the changes to Arches with:


.. code-block:: bash

    python manage.py etl_module unregister --source /projects/my_project/my_project/etl_modules/sample_etl_module.py
