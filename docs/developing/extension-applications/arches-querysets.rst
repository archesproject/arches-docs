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

As of Arches 8.2.0, **Arches Querysets** ships with Arches itself as ``arches.extensions.querysets``. There is nothing to install: enable it by adding it to ``INSTALLED_APPS``, along with the supporting settings described in :ref:`Applications Bundled with Arches`.

On Arches 8.0 and 8.1, the application is installed separately into the Python virtual environment of your Arches instance, and you will then need to edit your Arches instance's ``settings.py`` and other files. Those installation instructions can be found here: `Arches Querysets (Pypi) <https://pypi.org/project/arches-querysets>`_. The source code repository and issue tracking is available here: `Arches Querysets <https://github.com/archesproject/arches-querysets>`_ 
