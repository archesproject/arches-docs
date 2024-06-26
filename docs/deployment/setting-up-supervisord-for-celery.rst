.. _setting-up-supervisord-for-celery:

#################################
Setting up Supervisord for Celery
#################################

Arches uses Celery (https://docs.celeryq.dev/en/stable/getting-started/introduction.html), a Python framework for setting up and managing task queues. Using Celery,
Arches can delegate certain tasks with long execution times to separate processes. In a production deployment, this can enable Arches to delegate big jobs to a
queue so that requests to the Arches application do not lead to timeout or other errors.

This documentation discusses how to enable Celery task management using Supervisord (http://supervisord.org/). Essentially, Supervisord automatically monitors and controls Celery workers, checking to make sure they are operating, and restarting them if they fail.


When Do I Need Supervisord and Celery?
======================================
Arches *does not require* Supervisord and Celery to run in "production" mode (with ``DEBUG=False`` in `settings.py`). Arches instances managing smaller amounts of data may not need Supervisord and Celery. The deployment scenarios where you *should* consider using Supervisord and Celery include:

 * Supervisord and Celery will be required if you want to enable export / bulk download of more than 2000 resource instances.
 * Supervisord and Celery will be required to enable the Bulk Data Manager plugin to function. (Note: by default, Arches installs this plugin in hidden state.)



Supervisor and Celery Installation and Configuration
====================================================
The following is a guide **for a linux-based** OS; be advised you can change any of the file names, destinations, or permissions to suit your needs.


1. Supervisor can be installed using in your Arches virtual environment with ``pip``: ``pip install supervisor``.


2. In the core arches repo, in `arches/install/supervisor_celery_setup <https://github.com/archesproject/arches/tree/master/arches/install/supervisor_celery_setup>`_ there exist example files for supervisor, celeryd, and celerybeat. We recommend copying them into the following directory structure:

    .. code-block:: bash

        /etc/supervisor/
        |-- my_proj_name-supervisord.conf
        |-- conf.d/
        |    |-- my_proj_name-celeryd.conf
        |    |-- my_proj_name-celerybeat.conf


3. In the content of the files as well as the filenames themselves, replace the values of the following placeholders:

 * ``/absolute/path/to/virtualenv/`` - absolute path to your python3 virtualenv
 * ``[app]`` - replace this with the value of ``ELASTICSEARCH_PREFIX`` in your project’s ``settings.py`` file
 * ``/absolute/path/to/my_proj`` - absolute path to your arches project
 * ``my_proj_name`` - name of your project


4. Note that you can change the value for ``user`` in the ``-supervisord.conf`` file to a designated user to run supervisord.


5. Before proceeding, you will want to make sure that whichever user you designate to run supervisor has the appropriate permissions for the following files:

 * ``/var/log/supervisor/supervisord.log``
 * ``/var/log/celery/worker.log``
 * ``/var/log/celery/beat.log``
 * ``/var/run/supervisord.pid``


6. Download and install RabbitMQ: https://www.rabbitmq.com/download.html


7. Once successfully installed (and verified that it has been added to your PATH), start running it with the command ``rabbitmq-server``. For a convenient option, this can be run in a screen. Note that rabbitmq should be run prior to running supervisord. If you choose, you can use Redis as a "broker" instead of RabbitMQ (see below).


8. Run ``supervisord -c /etc/supervisor/my_proj_name-supervisord.conf`` to start the supervisord which will start celery workers for your tasks.


9. To check and stop your supervisord process, please review the following:

    a. To check on the status of celery (workers): ``supervisorctl -c /etc/supervisor/my_project-supervisor.conf status``
    b. To restart celery workers: ``supervisorctl -c /etc/supervisor/my_project-supervisor.conf restart celery``
    c. To stop celery workers: ``supervisorctl -c /etc/supervisor/my_project-supervisor.conf stop celery``
    d. To shut down supervisord (and the celery processes it controls): ``unlink /tmp/supervisor.sock``


Setting up Redis Instead of RabbitMQ
------------------------------------
Redis can serve as an alternative to RabbitMQ, but it lacks official Windows support. If you are not deploying Arches on Windows, you can use Redis as follows:

1. Follow the above directions (steps 1 to 5) for setting up supervisored, celery, and their configurations
2. Install Redis (see: https://redis.io/docs/getting-started/)
3. Install the Python interface to Redis into your Arches virtual environment with ``pip``: ``pip install redis``
4. Configure the `CELERY_BROKER_URL` (in `settings.py` or overwritten in `settings_local.py`): ``CELERY_BROKER_URL = "redis://@localhost:6379/0"``
5. Activate Redis: ``redis-server``
6. Run ``supervisord -c /etc/supervisor/my_proj_name-supervisord.conf`` to start the supervisord and celery workers
7. Start Arches

Known Issue with Arches Celery Configurations and Celery Beat
-------------------------------------------------------------
The default configuration files in the `conf.d` directory discussed above need updating. Version 5 and later of celery has a revised order of arguments in using celery commands (see: https://github.com/archesproject/arches/issues/9202).

    * The corrected syntax (celery >= v5x) for the command at the top of `my_proj_name-celeryd.conf` looks like:
      ``/absolute/path/to/virtualenv/bin/celery -A my_proj_name.celery worker --loglevel=INFO``

    * The corrected syntax (celery >= v5x) for the command at the top of `my_proj_name-celerybeat.conf` looks like (all in one line):
      ``/absolute/path/to/virtualenv/bin/celery -A my_proj_name.celery beat``
      ``--schedule=/tmp/celerybeat-schedule --loglevel=INFO --pidfile=/tmp/celerybeat.pid``

After fixing the command syntax, the celery worker should function. However, you may still have trouble getting celery beat to work (https://github.com/archesproject/arches/issues/9243). Celery beat schedules periodic tasks (much like a `crontab` in a Linux operating system) using a Python implementation. In many cases, Arches will function without (evident) problems even if celery beat does not work. However, if you have workarounds or fixes, please let us know!


Restart ``supervisord`` on Reboot
---------------------------------

On linux-based systems you can use a cronjob to ensure that supervisor starts whenever your system is rebooted. Note that you'll need to provide the full path to the virtual environment where you installed supervisor. To ensure that supervisor starts whenever your system is rebooted, you will need to edit your crontab (`see directions for Ubuntu <https://askubuntu.com/questions/609850/what-is-the-correct-way-to-edit-a-crontab-file>`_) and add a line similar to this example:


.. code-block:: crontab

  @reboot /absolute/path/to/virtualenv/bin/supervisord -c /etc/supervisor/my_proj_name-supervisord.conf




More information
----------------
 * Supervisord documentation: http://supervisord.org/
 * Celery sample files for supervisord: https://github.com/celery/celery/tree/master/extra/supervisord
 * Redis: https://redis.io/
 * Redis (Python interface): https://pypi.org/project/redis/