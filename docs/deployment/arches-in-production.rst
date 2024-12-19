
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


More HTTPS Security Settings
============================
The ``CSRF_TRUSTED_ORIGINS`` setting permits one to allow CSRF requests from specific origins. One can permit (encryption free) ``HTTP`` requests, but this should be discouraged because ``HTTP`` requests are not secure. In many deployment scenarios (when you deploy Arches behind a proxy or a cloud load balancer), one should also set the ``SECURE_PROXY_SSL_HEADER`` setting to ensure that Django is aware of the proxy's HTTPS status. In ``settings.py`` (sometimes set via ``settings_local.py``) you add this setting with the following code:

.. code-block:: python
  
  SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTOCOL", "https")

The ``SECURE_PROXY_SSL_HEADER`` setting is used to determine the actual request is secure. This setting is described in more detail in the `Django documentation <https://docs.djangoproject.com/en/4.2/ref/settings/#secure-proxy-ssl-header>`_.



Check Security Settings
=======================

The Django component of Arches has a number of security settings, and these settings can change as you upgrade Arches (including dependency Django libraries). You can find a list of these settings in the `Django documentation <https://docs.djangoproject.com/en/4.2/ref/settings/#security>`_. You can check the settings of your production Arches instance by running the following command:

.. code-block:: bash

  python manage.py check --deploy --tag=security


This command provides a current list of security-related settings that you should be aware of. You can then adjust these settings in your ``settings.py`` file (or ``settings_local.py``) as needed. An example of the output of this command is shown below:

.. code-block:: bash

  System check identified some issues:

  WARNINGS:
  ?: (security.W004) You have not set a value for the SECURE_HSTS_SECONDS setting. If your entire site is served only over SSL, you may want to consider setting a value and enabling HTTP Strict Transport Security. Be sure to read the documentation first; enabling HSTS carelessly can cause serious, irreversible problems.
  ?: (security.W008) Your SECURE_SSL_REDIRECT setting is not set to True. Unless your site should be available over both SSL and non-SSL connections, you may want to either set this setting True or configure a load balancer or reverse-proxy server to redirect all connections to HTTPS.
  ?: (security.W012) SESSION_COOKIE_SECURE is not set to True. Using a secure-only session cookie makes it more difficult for network traffic sniffers to hijack user sessions.
  ?: (security.W016) You have 'django.middleware.csrf.CsrfViewMiddleware' in your MIDDLEWARE, but you have not set CSRF_COOKIE_SECURE to True. Using a secure-only CSRF cookie makes it more difficult for network traffic sniffers to steal the CSRF token.
  ?: (security.W018) You should not have DEBUG set to True in deployment.
  ?: (security.W020) ALLOWED_HOSTS must not be empty in deployment.
  Arches: (arches.W001) Cache backend does not support rate-limiting
          HINT: Your cache: django.core.cache.backends.locmem.LocMemCache
          Supported caches: ('django.core.cache.backends.memcached.PyLibMCCache', 'django.core.cache.backends.memcached.PyMemcacheCache', 'django.core.cache.backends.redis.RedisCache')


Enable a Cache backend
----------------------
In the ``python manage.py check --deploy --tag=security`` output above, you will see a warning that the cache backend does not support rate-limiting. This is because the default cache backend in Django is ``LocMemCache``, which is an in-memory cache that does not support rate-limiting. To enable rate-limiting, you will need to configure a cache backend that supports rate-limiting. An example cache backend that supports rate-limiting for a production deployments is ``django.core.cache.backends.memcached.PyLibMCCache``. To enable this cache backend, add (and modify as needed for your deployment) the following to your ``settings.py`` file (or ``settings_local.py``):

.. code-block:: python

  CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211'
    },
}


Rate limiting
-------------
In addition to cache and rate-limit related settings to Arches, you should also consider implementing rate-limting configurations for proxy servers and load balancers. Such settings can intercept abusive levels of traffic *before* they start to interfere with the normal functioning of your Arches instance. In setting such configurations, you will to accomodate a "burst" rate, since a user's web browser interacting with Arches will (legitimately) make many requests over a short period of time. An example configuration for rate-limiting in Nginx can look something like this:

.. code-block:: nginx

  limit_req_zone $binary_remote_addr zone=general:10m rate=2r/s;

  server {
      location / {
          limit_req zone=general burst=20;
      }
  } 



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