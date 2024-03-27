###########################################
Orientation to Arches Use of the Django ORM
###########################################

Arches is built on Django, a powerful, popular, well-supported and well-documentant Python language web framework. This guide is intented to help guide developers already familiar with Django to better understand the Arches backend. The main focus here will center on how Arches uses the `Django Object Relational Model (ORM) <https://docs.djangoproject.com/en/5.0/topics/db/models/>`_ to power a highly configurable (and semantic, if one chooses to use ontologies) abstract :ref:`Data Model`. 

The Arches :ref:`Data Model` documentation provides an invaluable reference to understand Arches implementations of Django ORM models. This page provides more of a "guided tour" that illustrates how the Arches information you see in browser may be reflected in Django `query sets <https://docs.djangoproject.com/en/5.0/topics/db/queries/#retrieving-objects>`_ and objects (individual records). 


Exploring a (Nearly) Empty Database
===================================
In this guide, we will start with a freshly installed and nearly empty Arches instance to make exploration easier. If you haven't yet installed Arches, please review and follow this guide. We will then use the Arches Designer to set up a simple Branch and a Resource Model. 



1. Build a Branch
-----------------
Use the Arches Graph designer to make a branch and a resource model. In this demonstration case, we're making a simple branch for "Name" with two child nodes ("Given Name" and "Surname"). 




2. Build a Resource Model
-------------------------
After publishing this new "Name" branch, we can use it to describe resource models. Here, we're in the process of adding the "Name" branch to a "Person" resource model.


