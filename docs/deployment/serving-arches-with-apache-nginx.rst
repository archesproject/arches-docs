###################################
Serving Arches with Apache or Nginx
###################################

.. sidebar:: Further Reference

    + `Django Documentation <https://docs.djangoproject.com/en/stable/howto/deployment/wsgi/modwsgi/#how-to-use-django-with-apache-and-mod-wsgi>`_

During development, it's easiest to use the Django webserver to view your Arches installation. However, once you are ready to put the project into production, you'll have to use a more efficient, robust, and secure webserver like Apache or Nginx.

Use of Apache or Nginx involves many considerations in common, including set-up of SSL certificates for HTTPS, set-up and permissions of static assets, and running the Arches Django application with a WSGI server. The following guide first two sections describes how to use Apache. The next section focuses on using Nginx:

+ :ref:`Configure Apache`

+ :ref:`Prepare the Arches Project for Apache`

+ :ref:`Configure Nginx`



Configure Apache
================


The following instructions work for Ubuntu; minor changes may be necessary for a different OS. This is a very basic Apache configuration, and more fine tuning will benefit your production installation.

1. Install Apache.

    .. code-block:: bash

       $ sudo apt-get install apache2

2. Install ``mod_wsgi``

    There are two ways to install ``mod_wsgi``. Both of the require you to start by installing the Apache and Python development headers.

    .. code-block:: bash

        $ sudo apt install apache2-dev python3-dev

    .. note::

        You may need to install the Python dev package specific to your Python version, e.g. ``python3.10-dev``.

    Now follow one of the following two options:

    **Install mod_wsgi directly into your Python virtual environment**

    .. code-block:: bash

        $ source /home/ubuntu/Projects/ENV/bin/activate
        (ENV)$ pip install mod_wsgi

    Generate the link path to ``mod_wsgi``.

    .. code-block:: bash

        (ENV)$ mod_wsgi-express module-config

    This command will produce two lines that look like

    .. code-block:: bash

        LoadModule wsgi_module "<your venv path>/lib/python3.10/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-x86_64-linux-gnu.so"
        WSGIPythonHome "<your venv path>"

    Copy these two lines, you will use them in step 3.

    **Install mod_wsgi system-wide**

    Alternatively, you can use ``apt`` to install at the system level:

    .. code-block:: bash

        $ sudo apt install libapache2-mod-wsgi-py3

    Note that the version of Python 3 installed at the system-level may need to match the version used to create the virtual environment pointed to in the config.
    For example, if ``libapache2-mod-wsgi-py3`` is compiled against Python 3.10, use Python 3.10 for your virtual environment.
    Installing ``mod-wsgi`` this way means you will not need to load it as a module in the Apaache .conf file.

3.  Create a new Apache .conf file

    Here is a basic Apache configuration for Arches. If using a domain
    like ``heritage-inventory.org``, name this file ``heritage-inventory.org.conf``,
    otherwise, use something simple like ``arches-default.conf``.

    The paths below are based on an example project in ``/home/ubuntu/Projects/my_project``.

    .. code-block::

        sudo nano /etc/apache2/sites-available/arches-default.conf

    Complete new file contents::

        # If you have mod_wsgi installed in your python virtual environment, paste the text generated
        # by 'mod_wsgi-express module-config' here, *before* the VirtualHost is defined.
        LoadModule wsgi_module "/home/ubuntu/Projects/ENV/lib/python3.10/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-x86_64-linux-gnu.so"
        WSGIPythonHome "/home/ubuntu/Projects/ENV"

        <VirtualHost *:80>

            WSGIApplicationGroup %{GLOBAL}
            WSGIDaemonProcess arches python-path=/home/ubuntu/Projects/my_project
            WSGIScriptAlias / /home/ubuntu/Projects/my_project/my_project/wsgi.py process-group=arches

            # May be necessary to support integration with possible 3rd party mobile apps
            WSGIPassAuthorization on

            ## Uncomment the ServerName directive and fill it with your domain
            ## or subdomain if/when you have your DNS records configured.
            # ServerName heritage-inventory.org

            <Directory /home/ubuntu/Projects/my_project/>
                Require all granted
            </Directory>

            # This section tells Apache where to find static files. This example uses
            # STATIC_URL = '/media/' and STATIC_ROOT = os.path.join(APP_ROOT, 'static')
            # NOTE: omit this section if you are using S3 to serve static files.
            Alias /media/ /home/ubuntu/Projects/my_project/my_project/static/
            <Directory /home/ubuntu/Projects/my_project/my_project/static/>
                Require all granted
            </Directory>

            # This section tells Apache where to find uploaded files. This example uses
            # MEDIA_URL = '/files/' and MEDIA_ROOT = os.path.join(APP_ROOT)
            # NOTE: omit this section if you are using S3 for uploaded media
            Alias /files/uploadedfiles/ /home/ubuntu/Projects/my_project/my_project/uploadedfiles/
            <Directory /home/ubuntu/Projects/my_project/my_project/uploadedfiles/>
                Require all granted
            </Directory>

            ServerAdmin webmaster@localhost
            DocumentRoot /var/www/html

            # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
            # error, crit, alert, emerg.
            # It is also possible to configure the loglevel for particular
            # modules, e.g.
            #LogLevel info ssl:warn
            # Recommend changing these file names if you have multiple arches
            # installations on the same server.
            ErrorLog /var/log/apache2/error-arches.log
            CustomLog /var/log/apache2/access-arches.log combined

        </VirtualHost>

4. Disable the default Apache conf, and enable the new one.

    .. code-block::

        $ sudo a2dissite 000-default
        $ sudo a2ensite arches-default
        $ sudo service apache2 reload

    Replace ``arches-default`` with the name of your new .conf file if needed.

At this point, you can try accessing your Arches installation in a browser, but
you're likely to get some kind of file permissions error. Continue to the next section.

.. important::
    With Apache serving Arches, any changes to a ``.py`` file (like ``settings.py``)
    will not be reflected until you reload Apache.

Prepare the Arches Project for Apache
=====================================

1. Set all file and directory permissions.

    Apache runs as the user ``www-data``, and this user must have write access to
    some portions of your Arches project.

    .. note::

        On CentOS, Apache runs as is ``httpd``, so substitute that for ``www-data`` herein.

    The ``arches.log`` file...

    .. code-block:: bash

        $ sudo chmod 664 /home/ubuntu/Projects/my_project/my_project/arches.log
        $ sudo chgrp www-data /home/ubuntu/Projects/my_project/my_project/arches.log

    The ``uploadedfiles`` directory...

    .. code-block:: bash

        $ sudo chmod 775 /home/ubuntu/Projects/my_project/my_project/uploadedfiles
        $ sudo chgrp www-data /home/ubuntu/Projects/my_project/my_project/uploadedfiles

    Or, if either ``arches.log`` or ``uploadedfiles`` doesn't yet exist, you can
    just allow ``www-data`` to create them at a later point by giving write access
    to your project directory.

    .. code-block:: bash

        $ sudo chmod 775 /home/ubuntu/Projects/my_project/my_project
        $ sudo chgrp www-data /home/ubuntu/Projects/my_project/my_project

    You should now be able to access your Arches installation in a browser, but
    there is one more important step.

2. Run ``collectstatic``.

    This Django command places `all` of the static files (CSS, JavaScript, etc.)
    used in Arches into a single location that a webserver can find. By default,
    they are placed in ``my_project/my_project/static``, based on ``STATIC_ROOT``.

    .. note::

        You can change ``STATIC_ROOT`` all you want, but be sure to update the
        Alias and Directory info in the Apache conf accordingly.

    .. code-block::

        (ENV)$ python manage.py collectstatic

    The first time this runs it will take a little while (~20k files), and may
    show errors/warnings that you can safely ignore.

    Finally, make sure Apache has write access to this static directory because
    `django-compressor` needs to update the `CACHE` contents inside it:

    .. code-block::

        $ sudo chmod 775 /home/ubuntu/Projects/my_project/my_project/static
        $ sudo chgrp www-data /home/ubuntu/Projects/my_project/my_project/static

    .. important::

        from now on, any time you change a CSS, JavaScript, or other static
        asset you must rerun this command.

You should now be able to view your Arches installation in a browser without
any issues.



Configure Nginx
===============

Many Django applications use the open source Nginx application as a proxy server. If you want to use nginx + uWSGI instead of Apache + mod_wsgi, you should start with `this tutorial <https://uwsgi-docs.readthedocs.io/en/latest/tutorials/Django_and_nginx.html>`_ . You can also use Nginx with Gunicorn (an increasingly popular way to securely run a Django application). To use Nginx and Gunicorn, please start with `this tutorial <https://realpython.com/django-nginx-gunicorn/#putting-your-site-online-with-django-gunicorn-and-nginx>`_.


If you're using Gunicorn, don't forget to first install it into the Python virtual environment you are using for Arches:

.. code-block:: bash

    $ # install gunicorn into your Arches virtual environment
    $ pip install gunicorn


As is the case with Apache, Nginx will need appropriate permissions to serve static files. Every time you run `collectstatic`, you may change the file permissions, and you may need to rerun the following:

.. code-block:: bash

    $ sudo chmod 755 /home/ubuntu/Projects/my_project/my_project/static
    $ sudo chgrp nginx /home/ubuntu/Projects/my_project/my_project/static


It's sometimes useful to have an example configuration to help get you started. This Nginx configuration can be used as a guide.

.. note::

    The configuration provided below asks Nginx to compress text files (css, javascript, etc). This may help to noticeably improve performance for the Arches user interface.


.. code-block:: nginx

    server_names_hash_bucket_size 64;
    proxy_headers_hash_bucket_size 512;
    server_names_hash_max_size 512;
    large_client_header_buffers 8 64k;
    proxy_read_timeout 3600;
    proxy_connect_timeout 3600;

    # Connect to the Arches Django app running with Gunicorn.
    upstream django {
        server localhost:8000;
    }

    # The not encrypted plain HTTP config
    server {
        listen 80;
        charset utf-8;
        server_name my-arches-project.org www.my-arches-project.org;

        location ^~ /.well-known/acme-challenge/ {
            default_type "text/plain";
            autoindex on;
            allow all;
            root /var/www/certbot/$host;
        }

        access_log /logs/nginx/access.log;
        error_log /logs/nginx/error.log;
        proxy_read_timeout 3600;

        proxy_set_header  X-Forwarded-Protocol  $scheme;
        gzip on;
        gzip_disable "msie6";
        gzip_vary on;
        gzip_proxied any;
        gzip_comp_level 6;
        gzip_buffers 16 8k;
        gzip_http_version 1.1;
        gzip_types text/plain text/css application/json application/ld+json
    application/geo+json text/xml application/xml application/xml+rss
    text/javascript application/javascript text/html;

        # Redirect to use HTTPS
        location / {
            return 301 https://$host$request_uri;
        }
    }

    # The encrypted HTTPS config
    server {
        listen       443 ssl;

        server_name my-arches-project.org www.my-arches-project.org;
        access_log /logs/nginx/ssl_access.log;
        error_log /logs/nginx/ssl_error.log;

        proxy_set_header  X-Forwarded-Protocol  $scheme;
        proxy_read_timeout 3600;

        ssl_certificate /etc/your-ssl-path/fullchain.pem;
        ssl_certificate_key /etc/your-ssl-path/privkey.pem;

        # NOTE! These other config files are not documented here
        include /etc/nginx/options-ssl-nginx.conf;
        ssl_dhparam /etc/nginx/sites/ssl/ssl-dhparams.pem;
        include /etc/nginx/hsts.conf;
        
        # NOTE! Be default, NGINX only allows a 1MB file upload.
        # The following config raises this to 100MB
        client_max_body_size 100M;

        # Ask Nginx to use gzip compression to send javascript, css, etc.
        gzip on;
        gzip_disable "msie6";
        gzip_vary on;
        gzip_proxied any;
        gzip_comp_level 6;
        gzip_buffers 16 8k;
        gzip_http_version 1.1;
        gzip_types text/plain text/css application/json application/ld+json
    application/geo+json text/xml application/xml application/xml+rss
    text/javascript application/javascript text/html;

        location ^~ /.well-known/acme-challenge/ {
            default_type "text/plain";
            autoindex on;
            allow all;
            root /var/www/certbot/$host;
        }

        # For the 'alias', use the correct path to the location where Arches
        # puts static files after 'collectstatic'. Like Apache (see above)
        # Nginx will also need permissions to serve the static files.
        location  /static/ {
            autoindex on;
            allow all;
            alias  /path_to_arches_static_files_after_collectstatic/;
            include  /etc/nginx/mime.types;
        }

        location @proxy_to_django {
            proxy_pass http://django;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_redirect off;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $server_name;
        }
    }
