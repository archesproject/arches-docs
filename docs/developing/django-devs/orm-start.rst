###########################################
Orientation to Arches Use of the Django ORM
###########################################

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



4. Use a Terminal to Explore the ORM
------------------------------------
Now that you have used the Arches user interface to define a branch, a resource model, and have used these to create a resource instance, we can turn our attention to exploring how this information is represented in the Arches implementation of the Django ORM.


