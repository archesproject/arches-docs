############################
Arches Use of the Django ORM
############################

Arches is built on Django, a powerful, popular, well-supported and well-documentant Python language web framework. This guide is intented to help guide developers already familiar with Django to better understand the Arches backend. The main focus here will center on how Arches uses the `Django Object Relational Model (ORM) <https://docs.djangoproject.com/en/5.0/topics/db/models/>`_ to power a highly configurable (and semantic, if one chooses to use ontologies) abstract :ref:`Data Model`. 

The Arches :ref:`Data Model` documentation provides an invaluable reference to understand Arches implementations of Django ORM models. This page provides more of a "guided tour" that illustrates how the Arches information you see in a browser may be reflected in Django `query sets <https://docs.djangoproject.com/en/5.0/topics/db/queries/#retrieving-objects>`_ and objects (individual records). 


Exploring a (Nearly) Empty Database
===================================
In this guide, we will start with a freshly installed and nearly empty Arches instance to make exploration easier. If you haven't yet installed Arches, please review and follow this :ref:`Installing` guide. To avoid permissions complications, login to your new Arches instance as an administrator (super user). We will then use the :ref:`Arches Designer` to set up a simple Branch and a Resource Model. 



1. Build a Branch
-----------------
Use the Arches Graph designer to make a branch and a resource model. In this demonstration case, we're making a simple branch for "Name" with two child nodes ("Given Name" and "Surname"). 

.. figure:: ../../images/dev/arches-designer-branch.png
    :width: 100%
    :align: center

    Arches Designer user interface to create a new "Name" branch.


2. Build a Resource Model
-------------------------
After publishing this new "Name" branch, we can use it to describe resource models. Here, we're in the process of adding the "Name" branch to a "Person" resource model.

.. figure:: ../../images/dev/arches-designer-resource-model.png
    :width: 100%
    :align: center

    Arches Designer user interface to create a new "Person" resource model.

This results in the "Person" resource model with a "Name" branch. After one clicks on the "Publish Graph" button, we can create business data. In our example, that business data will include resource instances (of the Person resource model) and names (configured with the Name branch). 



3. Add a Resource Instance
--------------------------
Using the "Add New Resource" user interface, we can add a Person resource instance with name information. Once you save your new resource instance, let's explore how the information is represented in the Django ORM used by Arches.

.. figure:: ../../images/dev/arches-new-resource-instance.png
    :width: 100%
    :align: center

    Adding a resorce instance



4. Open a Terminal to Explore the ORM
-------------------------------------
Now that you have used the Arches user interface to define a branch, a resource model, and have used these to create a resource instance, we can turn our attention to exploring how this information is represented in the Arches implementation of the Django ORM.

Assuming you’ve activated your virtual environment for Arches, use a terminal to open a shell into the Arches Django application:

.. code-block:: bash

    python manage.py shell


Your terminal should display something like this:

.. code-block:: python

    Python 3.11.8 (main, Mar 12 2024, 11:41:52) [GCC 12.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>>


5. Import Arches Models and Explore the GraphModel
--------------------------------------------------
Now we should import some of the key Django models used by Arches to organize data. After importing these models, we can investigate how Arches represents the "Name" branch and the "Person" resource model that we already created using the user interface.

.. code-block:: python

    Python 3.11.8 (main, Mar 12 2024, 11:41:52) [GCC 12.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    (InteractiveConsole)
    >>> from arches.app.models.models import ResourceInstance, TileModel, GraphModel


Let's first take a look at the GraphModel. The GraphModel is used to store records of both branches and resource models.


.. code-block:: python

    >>> gr_qs = GraphModel.objects.all()
    >>> gr_qs.count()
    3


You'll see we have 3 objects in our queryset to select all items from the GraphModel. But we only made one branch, and one resource model! Where does the other GraphModel object come from?

To answer this question, let's investigtate further by looking at an individual object from the query set. The ``.__dict__`` outputs the object as a dict, making it easier to see the information that it contains.

.. code-block:: python

    >>> gr_obj = gr_qs.last()  # Get the last object in this queryset
    >>> gr_obj.__dict__
    {'_state': <django.db.models.base.ModelState object at 0x7f40110d3350>, 
    'graphid': UUID('ff623370-fa12-11e6-b98b-6c4008b05c4c'), 
    'name': <arches.app.models.fields.i18n.I18n_String object at 0x7f40110d18d0>, 
    'description': <arches.app.models.fields.i18n.I18n_String object at 0x7f40110d2f50>, 
    'deploymentfile': None, 'author': ' ', 'deploymentdate': None, 'version': '', 'isresource': True, 
    'iconclass': 'fa fa-sliders', 'color': None, 
    'subtitle': <arches.app.models.fields.i18n.I18n_String object at 0x7f40110d3050>, 
    'ontology_id': None, 'jsonldcontext': None, 'template_id': UUID('50000000-0000-0000-0000-000000000001'), 
    'config': {}, 'slug': None, 'publication_id': UUID('e437751c-e234-11ee-a712-0242ac120005')}


That looks a little difficult to understand especially because the name attribute has an `I18n_String object <https://github.com/archesproject/arches/blob/stable/7.5.1/arches/app/models/fields/i18n.py>`_. The I18n_String object is used by Arches to support internationalization. One can see the I18n_String object with:

.. code-block:: python

    >>> gr_obj.name.value
    '{"en": "Arches System Settings"}'
    >>> gr_obj.name.__str__()
    'Arches System Settings'

As you can see, the value of the I18n_String object is a JSON formatted string. Language codes ("en" in this case) are used as keys to different multi-lingual strings. One can get the string value for an I18n_String object, in the default language, with ``__str__()``.  So to output a more legible overview of try GraphModel queryset, try:

.. code-block:: python

    >>> [(gr_obj.graphid, gr_obj.name.__str__(), gr_obj.isresource) for gr_obj in gr_qs]
    [(UUID('ff623370-fa12-11e6-b98b-6c4008b05c4c'), 'Arches System Settings', True), 
    (UUID('c5eba1b7-aa2e-45bd-abc1-4c64df1bc7e4'), 'Person', True), 
    (UUID('8d7926ae-dc3d-4f77-be06-cd8a9e03b01a'), 'Name', False)]


Now we have a more clear picture of what's contained in the GraphModel queryset. The 'Arches System Settings' object was created in the Arches installation process. The two GraphModel objects that we created ('Person' and 'Name') are also present in the GraphModel queryset. The ``isresource`` attribute indicates that the 'Person' GraphModel object is a resource model.

