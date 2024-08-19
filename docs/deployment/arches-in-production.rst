
#####################################
Introduction to Production Deployment
#####################################

This guide will walk you through the steps necessary to deploy Arches in a production environment. This guide assumes that you have already installed Arches and have a working Arches installation. If you have not yet installed Arches, please see the :ref:`Installing Core Arches`. We recommend review of `Django's recommended checklist <https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/>`_ for production deployments in order to better understand how to deploy your Arches instances in production environments.




Set DEBUG = False
=================

Most importantly, you should never run Arches in production with ``DEBUG = True``. Open your ``settings.py`` file (or ``settings_local.py``) and set ``DEBUG = False`` (just add that line if necessary).

Turning off the Django debug mode will:

1. Suppress the verbose Django error messages in favor of a standard 404 or 500 error page.

    You will now find Django error messages printed in your ``arches.log`` file.

    .. IMPORTANT:: Make sure you have ``500.htm`` and ``404.htm`` files in your project's templates directory!

2. Cause Django to stop serving static files.

    You must set up a real webserver, like Apache or Nginx, to serve your app. See :ref:`Serving Arches with Apache`.




Add Allowed Hosts, CSRF Trusted Origins, and Session Cookie Secure to Settings
======================================================

``ALLOWED_HOSTS`` acts as a critical safeguard against HTTP Host header attacks, ensuring that your Arches application only responds to valid hostnames. On the other hand, ``CSRF_TRUSTED_ORIGINS`` is instrumental in fortifying your application against Cross-Site Request Forgery (CSRF) attacks by specifying trusted origins for the submission of forms. Finally, ``SESSION_COOKIE_SECURE`` ensures that the cookie containing user authentication information is only transmitted over HTTPS. Each of these settings is required for Arches to work properly in production. These settings are described in more detail in the `Django documentation <https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts>`_.


1. *Allowed Hosts*: In ``settings.py`` (sometimes set via ``settings_local.py``) you will need to add multiple items to the list of ``ALLOWED_HOSTS``. Consider the following example:

.. code-block:: python

  ALLOWED_HOSTS = ["my-arches-site.org", "localhost", "127.0.0.1",]

In that example, "my-arches-site.org" is the public domain name. But the items "localhost", "127.0.0.1" are all local network locations where Arches is deployed. You may need all of these for Arches to work properly.

2. *CSRF Trusted Origins*: Django 4.0, a dependency of Arches 7.5, introduced further strictness to its CSRF checking by consulting the ``Origin`` header. In the ``settings.py`` (sometimes set via ``settings_local.py``) you will need to add multiple items to the list of ``CSRF_TRUSTED_ORIGINS``. If you don't include this, users will encounter CSRF error (403) when they attempt to login. See the `Django documentation for details <https://docs.djangoproject.com/en/5.0/releases/4.0/#csrf-trusted-origins-changes>`_. Note the following items (with the ``https://`` prefix):

.. code-block:: python

  CSRF_TRUSTED_ORIGINS = ["https://my-arches-site.org", "https://www.my-arches-site.org",]

3. *Session cookies*: Set ``SESSION_COOKIE_SECURE`` to ``True``.

.. code-block:: python

  SESSION_COOKIE_SECURE = True


Build Production Frontend Assets
================================

In deploying Arches in production, have a choice in how you bundle frontend assets (CSS, Javascript, etc).

You can use ``npm run build_development`` followed by ``manage.py collectstatic`` to provide unminified frontend bundles.
These will be larger files, so there will be a hit with respect to network performance.

Alternatively, you can build production assets for the frontend, which will be minified and therefore faster for
clients to download. To make production frontend assets, use the ``manage.py build_production`` management command
(this combines both ``npm run build_production`` and ``manage.py collectstatic``). Please note however, you will need
at least *8GB* of RAM for the production frontend asset build itself (and much more if you're also running the
database and backend Arches server on the same host), and you will need lots of time. Depending on your system
specifics, this can take multiple hours to complete.