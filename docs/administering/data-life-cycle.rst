#############################
Data Lifecycle Good Practices
#############################

Arches provides tools to support users in the management of complex data, especially in the cultural heritage sector. To use Arches successfully, organizations also need to devote time and resources to maintain Arches, the database managed by Arches, and any digital files (images, videos, 3D models, and other external files) that may also be managed by Arches.


Data Integrity Risk Management
==============================

This section of the documentation provides some guidance about how to maintain the integrity of your Arches managed data, especially during different project lifecycle transitions. Many of the sections below describe different scenarios where one should take preventative measures to reduce risks of data loss or corruption. As is the case with any data management application, there is always some level of risk for data loss. Risk include:

* Hardware failure
* Software bugs
* Unexpected interruptions in the execution of software operations
* User errors
* Administrative errors
* Hacking or intentional vandalism
* ...and other disasters 


Database Backups
----------------

The most important method to reduce risks of data loss center on backup strategies. There are multiple methods one can use to backup Arches managed data, but the most straightforward approach for normal backups is to make use of :ref:`PostgreSQL Utilities` for database backups and restoration. Elements of good backup strategies include:

* **Regular scheduling**: Databases can fail even during normal operations. Regular backups can limit adverse impacts.
* **Backups before transitional events**: Some operations can put data at risk, so you should perform backups ahead of time.
* **Testing of backup files**: You should check to make sure database backups can actually be restored successfully)
* **Storage of backups in multiple locations**: You should keep backups separated from your Arches instance so that compromise or failure in one location does not also damage your backups.
* **Awareness of data security needs for backup files**: If you manage sensitive data, your backup files need to be treated securely as sensitive data.


Filesystem Backups
------------------

If your Arches instance manages digital files on a file system (images, videos, 3D models, documents, etc.) you will also need strategies to backup these media assets. 



Maintaining Data Integrity Through Transitions
==============================================

While there's always some risk of a problem, risk levels can change as your project goes through different transitions. There are also cases where you may need to perform special operations using the Arches user interface, SQL commands, or Python code interacting with the Django ORM that involve an element of risk to data integrity. In this section we describe some of these scenarios and recommended risk reduction strategies. 


Version Upgrades and Migrations
-------------------------------


Managing Provisional Edits
--------------------------

Deleting Resources
------------------

Bulk Data Management
--------------------

Changes to the Graph
--------------------

Operations via the Django ORM
-----------------------------

Python developers may want to use the Arches implementation of the Django ORM (see :ref:`Arches Use of the Django ORM`) to modify data in their Arches instance. We encourage you to develop experience and familiarity with how Arches organizes data and uses the the Django ORM first, especially before attempting modifications data used in production deployments. In some scenarios, modifying data using Python operations on the Django ORM may lead to unexpected results and corruption of your data.

The safest approach to modifying data using Python and the Django ORM makes use of Arches' data validation and integrity logic. To leverage this logic, your Python code should make use of various proxy models (see `Django's documentation for proxy models <https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models>`_) that Arches defines. The proxy models defined by Arches often implement data validation and data integrity logic that help protect against data corruption. 

You can import proxy models (with their data validation and integrity logic) as below:

.. code-block:: python

    from arches.app.models.card import Card
    from arches.app.models.graph import Graph
    from arches.app.models.resource import Resource
    from arches.app.models.tile import Tile

    # The Concept class is NOT a proxy model, but it contains lots of logic
    # associated with Reference Data Manager concepts
    from arches.app.models.concept import Concept




Operations via SQL 
------------------

In theory, one can modify Arches managed data using SQL directly on the PostgreSQL database. However, if you are new to Arches, **we strongly recommend AGAINST modifying data using SQL**. Use of SQL to modify data may bypass important validation and data integrity checks that are implemented in the Arches Python application. Naively modifying the database directly with SQL operations may lead to unexpected results and corruption of your data.

You can more safely use SQL operations to *INSERT*, *UPDATE*, and *DELETE* data using "relational views" that can be activated for different nodegroups, branches, and resource models. The "relational views" feature implements some data integrity and validation checks (particularly around datatypes) as PostgreSQL functions, so in theory, this should be a relatively safe way to use SQL to modify Arches data. Even so, in order to be performant, the "relational views" do not have all the data modification validation logic and "guardrails" offered by the Arches user interface. We recommend first gaining a strong understanding of how datatypes are formatted - especially related resources and concepts. An incorrectly formatted concept can easily cause a resource to fail indexing. Read more about relational views and SQL here: :ref:`SQL Import`  

Even if you use the "relational views" features and have a very deep understanding of the Arches database schema and its validation and data integrity logic, we still strongly recommend that you export a full database dump as a safety measure prior to attempting modifications via SQL. 

Once you've made changes using SQL operations you will need to reindex the database with ElasticSearch. See :ref:`ElasticSearch Management` 


Database Backup Approaches
==========================


Arches Utilities
----------------


PostgreSQL Utilities
--------------------

PostgreSQL has powerful utilities (see `Backup and Restore <https://www.postgresql.org/docs/14/backup.html>`_) to quickly export and restore databases. One can use these utilities to dump and restore Arches databases. Assuming you have an Arches project named "my_project" (and that Arches project has a database with the same name, as is the default), you can export the entire database as below:

.. code-block:: bash

    # Export your Arches project ('my_project') to PostgreSQL 
    # binary export file called 'my_project.dump'  
    pg_dump -U postgres -h localhost -F c -b my_project > 'my_project-v7-5-2-2024-05-11.dump'


You'll need to modify the command above if your PostgreSQL database is on a different host, uses a different port, or if your Arches database has a different database name. Please review PostgreSQL documentation to understand the different backup and restore options and arguments available for use.

You should carefully manage your database dump files. Different versions of Arches will have different database schemas. If you want to restore an Arches database from a dump file, you will need to restore it to an instance of Arches running the same version of Arches. In the example above, the export file "my_project-v7-5-2-2024-05-11.dump" is named to include the Arches version number so this can be matched if restoration is needed.



Arches UUIDs and External (or Legacy) Identifiers
-------------------------------------------------





Use of Cloud Comupting Database Services
========================================

Automated Backups
-----------------

Security and Permissions
------------------------




Security and Managing Sensitive Information
===========================================




Data Archiving (With External Repositories)
===========================================