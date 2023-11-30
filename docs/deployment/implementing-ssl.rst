################
Implementing SSL
################

Secure Sockets Layer (SSL) enables the server to establish an encrypted link with its clients. This is more secure than using unencrypted communication. To implement SSL you will need a digital certificate which can be signed either by you or by a certificate authority. For more information about the SSL certificates please see `this article <https://www.kaspersky.com/resource-center/definitions/what-is-a-ssl-certificate>`_ . 

Implementing SSL on your server can be divided to two stages:

+ :ref:`Obtaining a SSL certificate`
+ :ref:`Configuring the webserver`


Obtaining a SSL certificate
***************************
SSL certificate can be signed either by you using your own private key or by a certificate authority. Each choices has its own prerequisites and consequences. 


Self signed
===========
A good guide about how to implement this using OpenSSL on Ubuntu 20.04 can be found `here <https://www.digitalocean.com/community/tutorials/how-to-create-a-self-signed-ssl-certificate-for-apache-in-ubuntu-20-04>`_.

.. note::
    This option allows you to implement SSL using your server's IP address without a domain name. However, when accessing the website using any modern browser the connection will be marked as not private.

.. image :: ../images/connection-not-private.png
    :target: _images/connection-not-private.png 

Signed by Let's encrypt
=======================

`Let's Encrypt <https://letsencrypt.org/>`_ *is a non-profit certificate authority run by Internet Security Research Group that provides X.509 certificates for Transport Layer Security encryption at no charge*. You can obtain a certificate from other certificate authorities too. Please keep in mind that some authorities require a fee for their services. 

.. note::
    For this option you will need a domain name to use for your website.

Install certbot
---------------
certbot is a tool that helps you obtain a certificate from Let's encrypt. `The official installation instructions for apache running on Ubuntu 20.04 can be found here. <https://certbot.eff.org/lets-encrypt/ubuntufocal-apache>`_


Configuring the webserver
*************************
To use the digital certificate in serving your website you need to modify the webserver configuration. You can modify the current configuration file to add the new configuration or create a new configuration file. In this guide we will use one file. 

Start by adding the domain as a variable at the top of the file as such

.. code-block::

    ServerName yourDomainName

Then modify the current configuration to redirect the requests from port 80 to port 443. You will need to add this code

.. code-block::

    RewriteEngine On
    RewriteCond %{SERVER_PORT} !^443$
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]

You can transfer all the configuration related to arches to the new virtual host 443 and change </path/to/your/certificate/> to reflect the location of your certificate. Your file should look like this

.. code-block::

    ServerName yourDomainName
    LoadModule wsgi_module "/home/ubuntu/Projects/ENV/lib/python3.8/site-packages/mod_wsgi/server/mod_wsgi-py37.cpython-37m-x86_64-linux-gnu.so"
    WSGIPythonHome "/home/ubuntu/Projects/ENV"
    <VirtualHost *:80>
        ServerName yourDomainName
        ServerAdmin webmaster@localhost

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # This is optional, in case you want to redirect people 
        # from http to https automatically.
        RewriteEngine On
        RewriteCond %{SERVER_PORT} !^443$
        RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]

    </VirtualHost>
    <VirtualHost *:443>
        WSGIPassAuthorization on
        WSGIDaemonProcess arches python-path=/home/ubuntu/Projects/my_project
        WSGIScriptAlias / /home/ubuntu/Projects/my_project/my_project/wsgi.py process-group=arches
        <Directory /home/ubuntu/Projects/my_project/>
                    Options Indexes FollowSymLinks
                    AllowOverride None
                    Require all granted
        </Directory>

        Alias /media/ /home/ubuntu/Projects/my_project/my_project/static/
        <Directory /home/ubuntu/Projects/my_project/my_project/static>
                    Options Indexes FollowSymLinks
                    AllowOverride None
                    Require all granted
        </Directory>

        Alias /files/uploadedfiles /home/ubuntu/Projects/my_project/my_project/uploadedfiles
        <Directory /home/ubuntu/Projects/my_project/my_project/files/uploadedfiles>
                    Options Indexes FollowSymLinks
                    AllowOverride None
                    Require all granted
        </Directory>

        ServerName yourDomainName
        ServerAdmin webmaster@localhost
        DocumentRoot /var/www/html

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        SSLEngine on
        SSLCertificateFile </path/to/your/certificate/>cert.pem
        SSLCertificateKeyFile </path/to/your/certificate/>privkey.pem
        SSLCACertificateFile </path/to/your/certificate/>chain.pem
    </VirtualHost>


Then you will need to enable the SSL and redirecting modules before you reload apache configuration 

.. code-block:: 

    sudo a2enmod ssl
    sudo a2enmod rewrite 

Now you can reload apache to access the new configuration

.. code-block:: 

    sudo service apache2 reload