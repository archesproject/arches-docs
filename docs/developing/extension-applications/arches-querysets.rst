======================
Arches Querysets (App)
======================

**Arches Querysets** is an Arches extension application designed to simplify development of software interactions with Arches managed data. Arches Querysets provides interfaces that closely align with `Django Querysets <https://docs.djangoproject.com/en/5.2/ref/models/querysets/>`_. Rather than interacting directly with the graph abstractions used in Arches, Arches Querysets enables developers to use node and nodegroup aliases to query Arches managed data using familiar and widely adopted conventions established by Django Querysets. 

Arches Querysets can be installed as a component of an Arches instance that runs on core Arches version 8 and higher.


Arches Querysets Tutorial
-------------------------

As a convenience for developers, Arches Querysets aligns with the conventions and patterns used by Django Querysets. For additional instructions and examples on how to use node and nodegroup aliases in Arches Querysets, see this tutorial: `Arches Queryset Tutorial (Python Notebook) <https://github.com/archesproject/arches-querysets/blob/main/docs/tutorial.ipynb>`_


Installing Arches Querysets
---------------------------
The **Arches Querysets** extension application needs to be installed in the Python virtual environment of your Arches instance. Once installed, you will need to edit your Arches instance's ``settings.py`` and other files. The complete installation instructions can be found here: `Arches Querysets README <https://github.com/archesproject/arches-querysets?tab=readme-ov-file#arches-querysets>`_ 
