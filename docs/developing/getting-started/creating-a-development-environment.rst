==================================
Creating a Development Environment
==================================

The following is our recommendation for creating an Arches environment that works well for developers. The first thing to consider is the general structure that will be in place, presumably all in the same directory:

**Runtime Content**

+ ``ENV/`` - A Python 3.11+ virtual environment (you can name this whatever you want).

+ ``arches/`` - The local clone of your fork of the `archesproject/arches <https://github.com/archesproject/arches>`_ repo, this part of the code is often referred to as "core Arches."

+ ``my_project/`` - The location of your Arches project. This is the app in which you will be making the majority of your customizations (new images, new template contents, new plugins, etc.).

**Database Configuration Storage**

+ ``my_package/`` - The location of your Arches package. Packages can store custom database definitions that you will create, and are loaded into a project through a one-time command line operation.

Setting Everything Up
=====================

Core Arches
-----------

#. Install all :ref:`software dependencies <Software Dependencies>`, as well as `Git <https://git-scm.com/book/en/v2/Getting-Started-Installing-Git>`_.

    .. note::

        You may also be planning to use externally hosted components, like a remote Postgres/PostGIS or Elasticsearch installation. In that case make sure you have the connection information handy, you will need it in a later step.

#. :ref:`Create a new Python 3.11+ virtual environment <Create a Virtual Environment>`.

#. Clone the core Arches repo

    We recommend that you clone **your own fork** of the repo, but you can also clone `archesproject/arches <https://github.com/archesproject/arches>`_ if you don't plan to contribute code.

    .. code-block:: bash

        (ENV)$ git clone https://github.com/archesproject/arches
        (ENV)$ cd arches

#. Switch to the desired branch

    You can switch between versions of core Arches by changing to whichever branch you want. For example::

        (ENV)arches/$ git fetch
        (ENV)arches/$ git checkout stable/6.0.0
    
    will give you the stable branch for the 6.0.0 release.

#. Install the local core Arches

    This is **instead of** using ``pip install arches`` which would install the pypi Arches distribution directly into ``ENV``. When you install the local clone as shown below, any code changes you make inside of ``arches/`` (like checking out a new ``git`` branch) will be immediately reflected in your runtime environment.

    .. code-block:: bash

        (ENV)arches/$ pip install -e '.[dev]'
        (ENV)arches/$ pre-commit install
        (ENV)arches/$ git config blame.ignoreRevsFile .git-blame-ignore-revs
        (ENV)arches/$ cd ..

    .. note::

        If you later switch to a new git branch, you may need to uninstall and reinstall, as the Python dependencies do change over the course of Arches releases.

The Project
-----------

You can now head to :ref:`Creating a New Arches Project` to proceed through the project creation and database setup steps. 

Additionally, we recommend that you turn the new project into a git repo, which aids development and deployment. Keep in mind:

+ A ``.gitignore`` file will already be generated in your project.
+ Make sure all sensitive information (db credentials, API keys, etc.) is stored in ``settings_local.py``, **not** ``settings.py``.
+ Run ``pre-commit install`` from the project root to benefit from auto-fixes for linting and formatting.

The Package (optional)
----------------------

Think of the packages as external storage for complex database configurations like Resource Models, or custom components like Datatypes. A package allows you to back up and share this type of content outside of the project itself. In some cases, however, projects and packages can become interdependent.

Look at :ref:`Understanding Packages` for more information on how to create and maintain packages.

Overwriting Core Arches Content
===============================

In your project you can overwrite core Arches functionality in many ways. In general, doing so is preferable to directly altering any code in core Arches.

CSS (basic)
-----------

To overwrite existing (or add your own) style rules, create ``project.css`` in your project's media directory like this: ``my_project/my_project/media/css/project.css`` and place style content in there. By default, these rules are linked in the base Arches UI templates. To use these same rules on the splash page, add

.. code-block:: HTML

    <link href="{% static 'css/project.css' %}" rel="stylesheet">

to the bottom of the ``<head>`` tag in ``my_project/my_project/templates/index.htm``.

Templates (.htm) and JS (.js) (intermediate)
--------------------------------------------

For static files such as these, if you create a file in your project that matches the relative directory structure and name of that same file in core Arches, Django will inherit your new file and ignore the original Arches one.

.. note::

    To add new Javascript libraries to your project, see :ref:`Adding Javascript Dependencies`.

Dynamic Content (advanced)
--------------------------

It is much more complex to override dynamic content like a core Arches **view**, but entirely possible. For example, you could create ``views.py`` in your project and define a new view class in it like this, which inherits a core Arches view class.

.. code-block:: python

    from arches.app.views.user import UserManagerView

    class MyUserManagerView(UserManagerView):
        ## add a random print statement to make sure this class is used
        print("in MyUserManagerView")
        pass

and then in your ``urls.py``, change

.. code-block:: python

    urlpatterns = [
        path("", include("arches.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

to

.. code-block:: python

    from .views import MyUserManagerView

    urlpatterns = [
        # match and return your custom view before the default Arches url can get matched.
        path("user/", MyUserManagerView.as_view(), name="user_profile_manager"),
        path("", include("arches.urls")),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

which will cause /user to match your new view before the core Arches /user url is found. Thus, going to ``localhost:8000/user`` will still return the default Arches profile manager page, but it has been passed through your class. You can now add a ``get()`` method to your class and it will be called to return the view instead of ``arches.app.views.user.UserManagerView().get()``.

.. note::

    Remember: Arches is built with Django, so your best resource for more in-depth customization of projects is the `Django documentation <https://docs.djangoproject.com/>`_ itself.

.. warning::

    As a rule of thumb, the more complex the customizations are that you add to a project, the more difficult it will be retain these changes when you upgrade to later core Arches versions.

Handling Upgrades
=================

With the local clone of core Arches linked to your virtual environment, you can upgrade by simply pulling the changes to your local clone of the repo, or switching to a new release branch.

To upgrade projects, check the `release notes <https://github.com/archesproject/arches/releases>`_ which typically contain detailed instructions.

In general, you should always expect to

1) Reinstall Python dependencies in core Arches::

    (ENV)$ cd arches
    (ENV)arches/$ pip install '.[dev]'

2) Apply database migrations in ``my_project``::

    (ENV)$ cd my_project
    (ENV)my_project/$ python manage.py migrate

3) Reinstall javascript dependencies in ``my_project/my_project``::

    (ENV)$ cd my_project/my_project
    (ENV)my_project/my_project$ npm install

**Finally**, if you have added custom logic or content to your project, you must make sure to account for any changes in the core Arches content that you have overwritten or inherited.

Running Tests
=============

Tests must be run from core Arches. Enter ``arches/`` and then use::

    (ENV)arches/$ python manage.py test tests --settings="tests.test_settings"

It is possible that you will need to add or update ``settings_local.py`` inside of ``arches/`` in order for the tests to connect to Postgres and Elasticsearch.
