#################
Set DEBUG = False
#################

Most importantly, you should never run Arches in production with ``DEBUG = True``. Open your ``settings.py`` file (or ``settings_local.py``) and set ``DEBUG = False`` (just add that line if necessary).

Turning off the Django debug mode will:

1. Suppress the verbose Django error messages in favor of a standard 404 or 500 error page.

    You will now find Django error messages printed in your ``arches.log`` file.

    .. IMPORTANT:: Make sure you have ``500.htm`` and ``404.htm`` files in your project's templates directory!

2. Cause Django to stop serving static files.

    You must set up a real webserver, like Apache or Nginx, to serve your app. See :ref:`Serving Arches with Apache`.


################################
Build Production Frontend Assets
################################

In deploying Arches in production, have a choice in how you bundle frontend assets (CSS, Javascript, etc).

You can use ``yarn build_development`` followed by ``manage.py collectstatic`` to provide unminified frontend bundles.
These will be larger files, so there will be a hit with respect to network performance.

Alternatively, you can build production assets for the frontend, which will be minified and therefore faster for
clients to download. To make production frontend assets, use the ``manage.py build_production`` management command
(this combines both ``yarn build_production`` and ``manage.py collectstatic``). Please note however, you will need
at least *8GB* of RAM for the production frontend asset build itself (and much more if you're also running the
database and backend Arches server on the same host), and you will need lots of time. Depending on your system
specifics, this can take multiple hours to complete.