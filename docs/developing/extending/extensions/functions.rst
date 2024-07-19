#########
Functions
#########

Functions are the most powerful extension to Arches. Functions
associated with a Resource are called during various CRUD operations,
and have access to any server-side model. Proficient Python/Django
developers will find few limitations extending an Arches Project with
Functions.

Function must be created, registered, and then associated with a
Resource Model.

Functions are similar to database triggers. On get, save, post_save, 
and delete operations of a tile, the Python code in a function is run. 
For example, the primary descriptor function saves the primary descriptors 
of a resource model on the save event of a tile. Hypothetically, you could 
also do something like update an external system on the creation of a 
tile or send an email notification.

It is important to note that functions are **not run** during import operations 
(with the exception of non-bulk import via the command line interface, see 
:ref:`Import business data`). 


Primary Descriptors
===================
Functions are used to make **primary descriptors**. The primary descriptors function 
is used to generate the name of the resource, which is used to identify the resource 
in places such as the search results card, map popup and report title. It is also 
used to generate the resource descriptions displayed in the body of the search 
results and map popup cards.

The resource descriptors are generated on resource instance save. They can also be
regenerated for all the resources of a particular type by running the elasticsearch 
reindex management command with the ``--recalculate-descriptors`` flag. A description 
of the elasticsearch management commands can be found here: 
:ref:`ElasticSearch Management`


Creating a Function
===================

A Function comprises three separate files, which should be seen as
front-end/back-end complements. On the front-end, you will need a
component made from a Django HTML template and JavaScript pair, which
should share the same basename.

In your Project, these files must be placed like so:

    ``/myproject/myproject/media/js/views/components/functions/spatial_join.js``
    ``/myproject/myproject/templates/views/components/functions/spatial_join.htm``

The third file is a Python file which contains a dictionary telling
Arches some important details about your Function, as well as its main
logic.

    ``/myproject/myproject/functions/spatial_join.py``

.. note::

   As in the example above, its advisable that all of your files share
   the same basename. (If your Function is moved into a Package, this
   is necessary.) A new Project should have an example function in it
   whose files you can copy to begin this process.


Defining the Function's Details
===============================

The first step in creating a function is defining the ``details`` that
are in the top of your Function's ``.py`` file.

.. code-block:: python

    details = {
        'name': 'Sample Function',
        'type': 'node',
        'description': 'Just a sample demonstrating node group selection',
        'defaultconfig': {"selected_nodegroup":""},
        'classname': 'SampleFunction',
        'component': 'views/components/functions/sample-function'
    }



:name: **Required** Name is used to unregister a function, and shows up
       in the ``fn list`` command.
:type: **Required**  As of version 4.2, this should always be set to ``node`` or ``primarydescriptors``
:description: **Optional**  Add a description of what your Function does.
:defaultconfig: **Required** A JSON object with any configuration needed to
                serve your function's logic
:classname: **Required** The name of the python class that holds this
            Function's logic.
:component: **Required** Canonical path to html/js component.


More about the ``defaultconfig`` field
--------------------------------------

Any configuration information you need your Function to access can be
stored here. If your function needs to calculate something based on
the value of an existing Node, you can refer to it here. Or, if you
want your Function to e-mail an administrator whenever a specific node
is changed, both the Node ID and the email address to be used are good
candidates for storage in the ``defaultconfig`` dictionary.

The ``defaultconfig`` field serves both as a default, and as your
user-defined schema for your function's configuration data. Your
front-end component for the function will likely collect some of this
configuration data from the user and store it in the ``config``
attribute of the pertinent ``FunctionXGraph``.


Writing your Function Logic
===========================

In your Function's Python code, you have access to all your
server-side models. You're basically able to extend Arches in any way
you please. You may want to review the :ref:`Data Model`
documentation.


Function Hooks
==============

Your function needs to extend the ``BaseFunction`` class. Depending on
what you are trying to do, you will need to implement the ``get``,
``save``, ``post_save``, ``delete``, ``on_import``, and/or ``after_function_save``
methods.

.. code-block:: python

    class MyFunction(BaseFunction):

        def get(self, *args, **kwargs):
            raise NotImplementedError

        def save(self, *args, **kwargs):
            raise NotImplementedError
        
        # occurrs after Tile.save
        def post_save(self, *args, **kwargs):
            raise NotImplementedError

        def delete(self, *args, **kwargs):
            raise NotImplementedError

        def on_import(self, *args, **kwargs):
            raise NotImplementedError

        # saves changes to the function itself
        def after_function_save(self, *args, **kwargs):
            raise NotImplementedError

.. note::

   Not all of these methods are called in the current Arches
   software. You can also leave any of them unimplemented, and the
   ``BaseFunction`` class will raise a ``NotImplementedError`` for
   you. Arches is designed to gracefully ignore these exceptions for
   functions.

   A detailed description of current functionality is below.


``save`` and ``delete``
-----------------------

The ``Tile`` object will look up all its Graph's associated Functions
upon being saved. Before writing to the database, it calls each
function's ``save`` method, passing itself along with the Django
``Request`` object. This is likely where the bulk of your function's
logic will reside.

The ``Tile`` object similarly calls each of its graph's
functions' ``delete`` methods with the same parameters. Here, you can
execute any cleanup or other desired side effects of a Tile's
deletion. Your ``delete`` implementation will have the same signature
as ``save``.


``after_function_save``
-----------------------

The Graph view passes a FunctionXGraph object to
``after_function_save``, along with the request.


The FunctionXGraph object has a ``config`` attribute which stores that
instance's version of the ``defaultconfig`` dictionary. This is a good
opportunity, for example, to programmatically manipulate the
Function's configuration based on the Graph or any other server-side
object.

You can also write any general logic that you'd like to fire upon the
assignment of a Function to a Resource.

``on_import``
-------------

The import module calls on_import if the file format is a
JSON-formatted Arches file, and passes an associated Tile object.

CSV imports do not call this hook.

The UI Component
================
Having implemented your function's logic, it's time to develop the
front-end components required to associate it with Resources and
provide any configuration data.

The component you develop here will be rendered in the Resource
Manager when you associate the function with a Resource, and this is
where you'll put any forms or other UI artifacts used to configure the
Function.

Developing your Function's UI component is very similar to developing
:ref:`Widgets`. More specific guidelines are in progress, but for now,
refer to the sample code in your project's
``templates/views/components/functions/`` directory, and gain a little
more insight from the ``templates/views/components/widgets/``
directory. The complementary JavaScript examples will be located in
``media/js/views/components/functions/`` and
``media/js/views/components/widgets`` directories.


Registering Functions
=====================

First, list the names of functions you already have registered:

    ``(ENV)$ python manage.py fn list``

Now you can register your new function with

    ``(ENV)$ python manage.py fn register --source <path to your function's .py file>``

For example:

.. code-block:: bash

    (ENV)$ python manage.py fn register --source /Documents/projects/mynewproject/mynewproject/functions/sample_function.py


Now navigate to the Function Manager in the Arches Designer to confirm
that your new function is there and functional. If it's not, you may
want to unregister your function, make additional changes, and
re-register it. To unregister your function, simply run

.. code-block:: bash

    (ENV)$ python manage.py fn unregister --name 'Sample Function'

All commands are listed in :ref:`Command Line Reference - Function Commands <function commands>`.

