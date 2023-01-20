#######
Widgets
#######

Widgets allow you to customize how data of a certain DataType is
entered into Arches, and further customize how that data is presented
in Reports. You might have several Widgets for a given DataType,
depending on how you want the Report to look or to match the context
of a certain Resource.

Widgets are primarily a UI artifact, though they are closely tied to
their underlying DataType.

To develop a custom Widget, you'll need to write three separate files,
and place them in the appropriate directories. For the appearance and
behavior of the Widget, you'll need a component made of a Django
template and JavaScript file placed like so:

    ``project_name/templates/views/components/widgets/sample-widget.htm``
    ``project_name/media/js/views/components/widgets/sample-widget.js``

To register and configure the Widget, you'll need a JSON configuration
file:

    ``project_name/widgets/sample-widget.json``


Configuring your Widget
=======================

To start, here is a sample Widget JSON file:

.. literalinclude:: ../../examples/sample-widget.json
   :language: json

The most important field here is the ``datatype`` field. This controls
where your Widget will appear in the Arches Resource Designer. Nodes
each have a DataType, and Widgets matching that DataType will be
available when you're designing your Cards. The value must match an
existing DataType within Arches.

You can also populate the ``defaultconfig`` field with any
configuration data you wish, to be used in your Widget's front-end
component.

Designing Your Widget
=====================

Your Widget's template needs to include three Django template "blocks"
for rendering the Widget in different contexts within Arches. These
blocks are called **form**, **config_form**, and **report**. As you might
guess from their names, **form** is rendered when your Widget appears on
a Card for business data entry, **config_form** is rendered when you
configure the Widget on a card when designing a Resource, and **report**
controls how data from your Widget is presented in a Report.

Here is an example:

.. literalinclude:: ../../examples/sample-widget.htm
   :language: htmldjango

To pull it all together, you'll need to write a complementary
JavaScript file. The Arches UI uses Knockout.js, and the best way to
develop your Widget in a compatible way is to write a Knockout
component with a ``viewModel`` corresponding to your Widget's ``view``
(the Django template).

Here is an example, continuing with our ``sample-widget``:

.. literalinclude:: ../../examples/sample-widget.js
   :language: JavaScript

Registering your Widget
=======================

After placing your Django template and JavaScript files in their
respective directories, you are now ready to register your Widget:


.. code-block:: bash

    python manage.py widget register --source /Documents/projects/mynewproject/mynewproject/widgets/sample-widget.json

The command will confirm your Widget has been registered, and you can
also see it with:

.. code-block:: bash

    python manage.py widget list

If you make an update to your Widget, you can load the changes to
Arches with:


.. code-block:: bash

    python manage.py widget update --source /Documents/projects/mynewproject/mynewproject/widgets/sample-widget.json

All the Widget commands are detailed in :ref:`Command Line Reference - Widget Commands <widget commands>`.
