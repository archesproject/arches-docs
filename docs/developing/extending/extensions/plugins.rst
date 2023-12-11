#######
Plugins
#######

Plugins allow a developer to create an independent page in Arches that is accessible from the main navigation menu.
For example, you may need a customized way of visualizing your resource data. A plugin would enable you to design such an interface.
Plugins, like widgets and card components rely only on front-end code. Ajax queries, generally calls to the API, must be used to access any server side data.

Registering your Plugin
===============================

To register your Plugin, you'll need a JSON configuration file
looking a lot like this sample:


.. literalinclude:: ../../../examples/sample-plugin.json
   :language: json


:pluginid:
        **Optional** A UUID4 for your Plugin. Feel free to generate
        one in advance if that fits your workflow; if not, Arches will
        generate one for you and print it to STDOUT when you register
        the Plugin.
:name:
        **Required** The name of your new Plugin, visible when a user hovers over the main navigation menu
:icon:
        **Required** The icon visible in the main navigation menu.
:component:
        **Required** The path to the component view you have
        developed. Example: ``views/components/plugins/sample-plugin``
:componentname:
        **Required** Set this to the last part of ``component`` above.
:config:
        **Required** You can provide user-defined default
        configuration here. Make it a JSON dictionary of keys and
        values. An empty dictionary is acceptable.
:slug: **Required** The string that will be used in the url to access your plugin
:sortorder: **Required** The order in which your plugin will be listed if there are multiple plugins


Plugin Commands
---------------

To register your Plugin, use this command:

.. code-block:: bash

    python manage.py plugin register --source /Documents/projects/mynewproject/mynewproject/plugins/sample-plugin.json

The command will confirm your Plugin has been registered, and you can
also see it with:

.. code-block:: bash

    python manage.py plugin list

If you make an update to your Plugin, you can load the changes to
Arches with:


.. code-block:: bash

    python manage.py plugin update --source /Documents/projects/mynewproject/mynewproject/plugins/sample-plugin.json
