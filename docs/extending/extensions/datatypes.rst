#########
Datatypes
#########

A DataType defines a type of business data. DataTypes are associated
with Nodes and Widgets. When you are designing your Cards, the Widgets
with the same DataType as the Node you are collecting data for will be
available. In your Branches, each Node with a DataType will honor the
DataType configuration you specify when you create it.

The simplest (non-configurable, non-searchable) DataTypes consist of a
single Python file. If you want to provide Node-specific configuration
to your DataType (such as whether to expose a Node with that DataType
to Advanced Search or how the data is rendered), you'll also develop a
UI component comprising a Django template and JavaScript file.

In your Project, these files must be placed accordingly:

    Optional Configuration Component:

    ``/myproject/myproject/media/js/views/components/datatypes/sample_datatype.js``
    ``/myproject/myproject/templates/views/components/datatypes/sample_datatype.htm``

    DataType File:

    ``/myproject/myproject/datatypes/sample_datatype.py``


To begin, let's examine the ``sample-datatype`` included with Arches:


.. literalinclude:: ../../examples/sample_datatype.py
   :language: python
   :linenos:


Writing Your DataType
=====================

Your DataType needs, at minimum, to implement the ``validate``
method. You're also likely to implement the
``transform_import_values`` or ``transform_export_values``
methods. Depending on whether your DataType is spatial, you may need
to implement some other methods as well. If you want to expose Nodes
of your DataType to Advanced Search, you'll also need to implement the
``append_search_filters`` method.

You can get a pretty good idea of what methods you need to implement
by looking at the ``BaseDataType`` class in the Arches source code
located at ``arches/app/datatypes/base.py`` and below:

.. literalinclude:: ../../examples/base.py
   :language: python
   :linenos:

the ``validate`` method
-----------------------

Here, you write logic that the Tile model will use to accept or reject
a Node's data before saving. This is the core implementation of what
your DataType is and is not.

The ``validate`` method returns an array of errors. If the array is
empty, the data is considered valid. You can populate the errors array
with any number of dictionaries with a ``type`` key and a ``message``
key. The value for ``type`` will generally be ``ERROR``, but you can
provide other kinds of messages.

the ``append_search_filters`` method
------------------------------------

In this method, you'll create an ElasticSearch query Nodes matching
this datatype based on input from the user in the Advanced Search
screen. (You design this input form in your DataType's front-end
component.)

Arches has its own ElasticSearch query `DSL builder class
<https://github.com/archesproject/arches/blob/master/arches/app/search/elasticsearch_dsl_builder.py>`_.
You'll want to review that code for an idea of what to do. The search
view passes your DataType a Bool() query from this class, which you
call directly. You can invoke its ``must``, ``filter``, ``should``, or
``must-not`` methods and pass complex queries you build with the DSL
builder's ``Match`` class or similar. You'll execute this search
directly in your ``append_search_filters`` method.

In-depth documentation of this part is planned, but for now, look at
the `core datatypes
<https://github.com/archesproject/arches/blob/master/arches/app/datatypes/datatypes.py>`_
located in Arches' source code for examples of the approaches you can
take here.

.. note::

   If you're an accomplished Django developer, it should also be
   possible to use Elastic's own `Python DSL builder
   <https://github.com/elastic/elasticsearch-dsl-py>`_ in your Project
   to build the complex search logic you'll pass to Arches' ``Bool()``
   search, but this has not been tested.

Configuring your DataType
=========================
You'll need to populate the ``details`` dictionary to configure your
new DataType.

.. literalinclude:: ../../examples/sample_datatype.py
   :language: python
   :lines: 7-17

:datatype:
        **Required** The name of your datatype. The convention in
        Arches is to use *kebab-case* here.
:iconclass:
        **Required** The FontAwesome icon class your DataType should
        use. Browse them `here
        <https://fontawesome.com/icons?d=gallery>`_.
:modulename:
        **Required** This should always be set to ``datatypes.py``
        unless you've developed your own Python module to hold your
        many DataTypes, in which case you'll know what to put here.
:classname:
        **Required** The name of the Python class implementing your
        datatype, located in your DataType's Python file below these
        details.
:defaultwidget:
        **Required** The default Widget to be used for this DataType.
:defaultconfig:
        **Optional** You can provide user-defined default
        configuration here.
:configcomponent:
        **Optional** If you develop a configuration component, put the
        fully-qualified name of the view here. Example:
        ``views/components/datatypes/sample-datatype``
:configname:
        **Optional** The name of the Knockout component you have
        registered in your UI component's JavaScript file.
:isgeometric:
        **Required** Used by the Arches UI to determine whether to
        create a Map Layer based on the DataType, and also for
        caching. If you're developing such a DataType, set this to
        True.
:issearchable:
        **Optional** Determines if the datatype participates in advanced search.
        The default is false.

.. important::

   ``configcomponent`` and ``configname`` are required together.

Developing the Configuration Component
======================================

Your component JavaScript file should register a Knockout component
with your DataType's ``configname``. This component should be an
object with two keys: ``viewModel``, and ``template``

The value for ``viewModel`` should be a function where you put the
logic for your template. You'll be setting up Knockout observable and
computed values tied to any form elements you've developed to collect
Advanced Search or Node-level configuration information from the user.

The value for ``template`` should be another object with the key
``require``, and the value should be
``text!datatype-config-templates/<your-datatype-name>``. Arches will
know what to do with this -- it comes from the value you supplied in
your Python file's ``details`` dictionary for ``configcomponent``.

Pulling it all together, here's the JavaScript portion of Arches'
``date`` DataType.

.. literalinclude:: ../../examples/date.js
   :language: javascript


Advanced Search Rendering
-------------------------

If you're supporting Advanced Search functionality for Nodes with your
DataType, your Django template will include a ``search`` block,
conditionally rendered by Knockout.js if the search view is
active. Here's the one from the ``boolean`` datatype:


.. literalinclude:: ../../examples/boolean.htm
   :language: htmldjango
   :lines: 2-10

Note the ``<!-- ko if: $data.search -->`` directive opening and
closing the search block. This is not an HTML comment -- it's
Knockout.js-flavored markup for the conditional rendering.

Arches' built-in ``date`` DataType does not use the Django template
``block`` directive, but only implements advanced search, and contains
a more sophisticated example of the component logic needed:


.. literalinclude:: ../../examples/date.htm
   :language: django


Node-specific Configuration
---------------------------

This section of your template should be enclosed in Knockout-flavored
markup something like: ``<!-- ko if: $data.graph -->``, and in your
Knockout function you should follow the convention and end up with
something like ``if (this.graph) {``

Here, you put form elements corresponding to any configuration you've
implemented in your DataType. These should correspond to keys in your
DataType's ``defaultconfig``.

Arches' ``boolean`` DataType has the following ``defaultconfig``:

.. code-block:: python

   {'falseLabel': 'No', 'trueLabel': 'Yes'}

You can see the corresponding data bindings in the Django template:

.. literalinclude:: ../../examples/boolean.htm
   :language: htmldjango
   :lines: 12-25

And finally, here is the ``boolean`` DataType's JavaScript file in its entirety:

.. literalinclude:: ../../examples/boolean.js
   :language: javascript

Registering your DataType
=========================

These commands are identical to working with Widgets, but you use the
word ``datatype`` instead. Please refer to :ref:`Command Line Reference - Widget Commands <widget commands>`.

