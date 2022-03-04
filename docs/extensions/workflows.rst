#########
Workflows
#########

Workflows are a type of :doc:`Plugin <plugins>` that can simplify the data entry process. A workflow is composed of one or more cards from a resource model, placing them in a step-through set of forms. This provides users the ability to create new resource instances without having to traverse card-by-card through the resource model tree.

Workflows can be complex too, facilitating the creation of many different inter-related resource instances simultaneously. We'll use a very simple example here, however, to show how a workflow can be used to extract just a few cards from a large resource model to facilitate a "quick create" task that is easy for users to complete.

In other words, instead of using this interface to create a new resource:

.. figure:: ../images/full-editor.jpg
    :width: 100%
    :align: center

    Default full resource editor.

...a workflow can pare down the data entry interface to look something like this:

.. figure:: ../images/quick-workflow-example.jpg
    :width: 100%
    :align: center

    A simple workflow abstracts data entry away from the card tree into forms.

Creating a Workflow - the Basics
================================

A very simple workflow will be presented here, based on the `arches-example-pkg <https://github.com/archesproject/arches-example-pkg>`_ resource model called "Heritage Resource Model". This resource model has many cards, but we will make a workflow that pulls just three of these cards out--Name/Name Type, Resource Type Classification, and Keyword.

Workflows follow the standard extension pattern: an HTML/JS component and a JSON config. For this example, we have::

    myproject/myproject/templates/views/components/plugins/quick-resource-create-workflow.htm
    myproject/myproject/media/js/views/components/plugins/quick-resource-create-workflow.js 

and::

    myproject/myproject/plugins/quick-resource-create-workflow.json

.. note:: Remember, Workflows are just a special subset of Plugins, so the two types of extensions will be stored alongside each other.

The JSON configuration looks like this:

.. literalinclude:: ../examples/quick-resource-create-workflow.json
    :language: json

The majority of the work is done by the creation of the workflow steps.

.. note:: Detailed description of this file's structure coming soon.

.. literalinclude:: ../examples/quick-resource-create-workflow.js
    :language: javascript

Finally, the HTML template exceptionally simple (just two lines):

.. literalinclude:: ../examples/quick-resource-create-workflow.htm
    :language: htmldjango

Registering your Workflow
==============================

After placing your workflow files in the proper directories within your project, you are ready to register them:

.. code-block:: bash

    python manage.py plugin register -s myproject/plugins/quick-resource-create-workflow.json

The command will confirm your workflow has been registered, and you can
also see it with:

.. code-block:: bash

    python manage.py plugin list

You can unregister the workflow like this:

.. code-block:: bash

    python manage.py plugin unregister -n "Quick Create Resource"

See :ref:`Command Line Reference` for more information.