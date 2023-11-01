***************
Card Components
***************

Beginning in Arches 4.3, Cards are rendered using Card Components,
allowing them to be composed and nested arbitrarily in various
contexts within the Arches UI. Arches comes with a default Card
Component that should suit most needs, but you can also create and
register custom Card Components to extend the front-end behavior of
Arches.

Before exploring how do make customized Cards, please review documentation
about available :ref:`Card Types` standard with Arches.


.. note:

   A Card Component is not a component of a card -- it is a
   Knockout.js component used to render a Card. Each Card Component is
   a UI representation of a card and contains Widgets, etc.


Developing Card Components is very similar to developing Widgets. A
Card Component consists of a Django template and Knockout.js
JavaScript file. To register your component, you'll also need a JSON
file specifying its initial configuration.

To develop your new card, you'll place files like so in your project:


    ``project_name/templates/views/components/cards/my-new-card.htm``
    ``project_name/media/js/views/components/cards/my-new-card.js``

To register and configure the Component, you'll need a JSON configuration
file:

    ``project_name/cards/my-new-card.json``


Creating a Card Component
=========================

The default template and Knockout files illustrate everything a Card
Component needs, and you'll be extending this functionality. Your
template will provide conditional markup for various contexts
('editor-tree', 'designer-tree', 'permissions-tree', 'form', and
'report'), render all the card's Widgets, and display other
information.


Here's the template for the default Card Component:

.. literalinclude:: ../examples/default-card.htm
   :language: htmldjango


And here's the Knockout file:

.. literalinclude:: ../examples/default-card.js
   :language: javascript



Registering your Card Component
===============================

To register your Component, you'll need a JSON configuration file
looking a lot like this sample:


.. literalinclude:: ../examples/new-card-component.json
   :language: json

:componentid:
        **Optional** A UUID4 for your Component. Feel free to generate
        one in advance if that fits your workflow; if not, Arches will
        generate one for you and print it to STDOUT when you register
        the Component.
:name:
        **Required** The name of your new Card Component, visible in
        the drop-down list of card components in the Arches Designer.
:description:
        **Required** A brief description of your component.
:component:
        **Required** The path to the component view you have
        developed. Example: ``views/components/cards/sample-datatype``
:componentname:
        **Required** Set this to the last part of `component` above.
:defaultconfig:
        **Required** You can provide user-defined default
        configuration here. Make it a JSON dictionary of keys and
        values. An empty dictionary is acceptable.



Card Commands
-------------

To register your Card Component, use this command:

.. code-block:: bash

    python manage.py card_component register --source /Documents/projects/mynewproject/mynewproject/cards/new-card-component.json

The command will confirm your Component has been registered, and you can
also see it with:

.. code-block:: bash

    python manage.py card_component list

If you make an update to your Card Component, you can load the changes to
Arches with:


.. code-block:: bash

    python manage.py card_component update --source /Documents/projects/mynewproject/mynewproject/cards/new-card-component.json

All the Card Component commands are detailed in :ref:`Command Line Reference - Card Component Commands <card component commands>`.
