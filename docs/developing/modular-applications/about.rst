#################################
About Arches Modular Applications
#################################

Starting with version 7.5 and 8, the Arches project adopted a more modular and less monolithic approach to software architecture.
Instead of integrating all new features into core Arches, the Arches project started to bundle sets of special purpose features as 
separate modular applications that administrators can choose to install onto an Arches instance. These special purpose modular
applications have their own code repositories and installation instructions.


Different Kinds of Arches Applications
======================================
The Arches project uses the term "application" in a number of different senses. Some **Arches applications** are comprehensive and
stand-alone software to meet the data management needs of a specific community. These comprehensive Arches applications are 
built on the foundation of core Arches and include extra data modeling, user interface, and other customizations. Comprehensive Arches
applications are stand-alone tools and are **not intended to combined as components** within a given Arches instance.  

Examples of (Comprehensive) Arches Applications
-----------------------------------------------
* `Arches for HERs <https://www.archesproject.org/arches-for-hers/>`_
* `Arches for Science <https://www.archesproject.org/arches-for-science/>`_
* `Arches for Reference and Sample Collections (RaSColls) <https://www.archesproject.org/rascolls/>`_



What's a (Modular) Application?
===============================

On the other hand, the term **Arches modular application (app)** describes a Python package (usually pip installed) that provides some set 
of additional features beyond what core Arches provides. Arches application can be reused as a modular component of multiple Arches 
projects.

Applications typically include some combination of models, views, templates, static files, URLs, etc. 
They're generally wired into Arches projects with the INSTALLED_APPS setting.


.. figure:: ../../images/dev/diagram-custom-apps-in-projects.png
    :width: 100%
    :align: center

    Illustration of Arches projects integrating custom Arches Application.



Examples of Arches Modular Applications (Apps)
----------------------------------------------
* `Arches Controlled Lists <https://github.com/archesproject/arches-controlled-lists>`_ See additional (:ref:`Arches Controlled Lists`) documentation.
* `Arches Modular Reports <https://github.com/archesproject/arches-modular-reports>`_
* `Arches Querysets <https://github.com/archesproject/arches-querysets>`_





