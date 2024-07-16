############################
Data Curation Good Practices
############################

Arches provides tools to support users in the management of complex data, especially in the cultural heritage sector. To use Arches successfully, organizations also need to devote time and resources to maintain Arches, the database managed by Arches, and any digital files (images, videos, 3D models, and other external files) that may also be managed by Arches.


Data Integrity Risk Management
==============================

This section of the documentation provides some guidance about how to maintain the integrity of your Arches managed data, especially during different project transitions. Many of the sections below describe different scenarios where one should take preventative measures to reduce risks of data loss or corruption. As is the case with any data management application, there is always some level of risk for data loss. Risk include:

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
* **Backups before transitional events**: Some operations (including software updates, bulk edits to the database, modifying graphs already populated with resource instances) can put data at risk, so you should perform backups before making such changes.
* **Testing of backup files**: You should check to make sure database backups can actually be restored successfully.
* **Storage of backups in multiple locations**: You should keep backups separated from your Arches instance so that compromise or failure in one location does not also damage your backups.
* **Awareness of data security needs for backup files**: If you manage sensitive data, your backup files need to be treated securely as sensitive data.


Database backups are an important security and risk reduction method for your Arches instance. However, database backups are *not* (by themselves) a long term data archiving and preservation strategy. Long term data preservation involves other requirements, processes, and organizational supports beyond backups. See the section :ref:`Data Archiving (with External Repositories)` to learn more about the long term preservation of Arches data.



ElasticSearch Backups
---------------------

It is most crucial to maintain a good backup strategy for your Arches data in PostgreSQL. However, if your Arches instance manages large amounts of data, it can be time consuming to rebuild an ElasticSearch index from scratch should this index fail. In these scenarios, you may also want to maintain backups of your ElasticSearch index (see ElasticSearch's `snapshot and restore documentation <https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshot-restore.html>`_). Ideally, one should carefully synchronize backups (and restorations) for *both* the Arches PostgreSQL database *and* the ElasticSearch index so that they maintain consistency. Otherwise, you may need to reindex ElasticSearch so it matches the state of the PostgreSQL database.


Filesystem Backups
------------------

If your Arches instance manages digital files on a file system (images, videos, 3D models, documents, etc.) you will also need strategies to backup these media assets. 



Maintaining Data Integrity Through Transitions
==============================================

While there's always some risk of a problem, risk levels can change as your project goes through different transitions. There are also cases where you may need to perform special operations using the Arches user interface, SQL commands, or Python code interacting with the Django ORM that involve an element of risk to data integrity. In this section we describe some of these scenarios and recommended risk reduction strategies. 


Version Upgrades and Migrations
-------------------------------

As a rule, one should make comprehensive backups of Arches databases *prior* to making software updates and version upgrades. 

The Arches core application has ongoing software development to add new features, improve performance, fix bugs and make other enhancements (see: :ref:`Arches Release Process`). Some of these software updates will involve changes to the Arches PostgreSQL database. In cases where software updates require changes to the database, Arches makes use of Django `"migrations" <https://docs.djangoproject.com/en/5.0/topics/migrations/>`_) to automatically update the PostgreSQL database. 

Database migrations may change certain database records, the database schema, or both. We recommend review of the release notes (see :ref:`Arches Releases`) associated with version update to understand the nature of these changes. **Follow all release notes instructions to upgrade your Arches project.** Because Arches version upgrades typically involve database migrations, we *strongly recommend that you backup your data* prior to attempting an upgrade. See :ref:`PostgreSQL Utilities` below to review PostgreSQL utilities for backing up and restoring your database.   



Managing Provisional Edits
--------------------------
*Forthcoming*


Deleting Resources
------------------
*Forthcoming*


Bulk Data Management
--------------------
*Forthcoming*


Changes to the Graph
--------------------
*Forthcoming*


Operations via the Django ORM
-----------------------------

Python developers may want to use the Arches implementation of the Django ORM (see :ref:`Arches Use of the Django ORM`) to modify data in their Arches instance. We encourage you to develop experience and familiarity with how Arches organizes data and how Arches uses the Django ORM first, especially before attempting modifications data used in production deployments. In some scenarios, naive use of Python and the Django ORM to modify data may lead to unexpected results and corruption of your data.

The safest approach to modifying data using Python and the Django ORM makes use of Arches' data validation and integrity logic. To leverage this logic, your Python code should make use of various proxy models (see `Django's documentation for proxy models <https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models>`_) that Arches defines. The proxy models defined by Arches often implement data validation and data integrity logic that help protect against data corruption. 

In Python, one can import proxy models (with their data validation and integrity logic) as below:

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

A developer can modify Arches managed data using SQL directly on the PostgreSQL database. However, if you are new to Arches, **we strongly recommend AGAINST modifying data using SQL**. Use of SQL to modify data may bypass important validation and data integrity checks that are implemented in the Arches Python application. Naively modifying the database directly with SQL operations may lead to unexpected results and corruption of your data.

You can more safely use SQL operations to *INSERT*, *UPDATE*, and *DELETE* data using "relational views" that can be activated for different nodegroups, branches, and resource models. The "relational views" feature implements some data integrity and validation checks (particularly around datatypes) as PostgreSQL functions, so in theory, this should be a relatively safe way to use SQL to modify Arches data. Even so, in order to be performant, "relational views" *do not have all* the data modification validation logic and "guardrails" offered by the Arches user interface. We recommend first gaining a strong understanding of how datatypes are formatted - especially related resources and concepts. An incorrectly formatted concept can easily cause a resource to fail indexing. Read more about relational views and SQL here: :ref:`SQL Import`  

Even if you use the "relational views" features and have a very deep understanding of the Arches database schema and its validation and data integrity logic, we still strongly recommend that you export a full database dump as a safety measure prior to attempting modifications via SQL. 

Once you've made changes using SQL operations you will need to reindex the database with ElasticSearch. See :ref:`ElasticSearch Management` 


Database Backup Approaches
==========================

Again, the most straightforward approach for normal backups is to make use of :ref:`PostgreSQL Utilities` for database backups and restoration. Because PostgreSQL is such a popular database application and is especially widely used in conjunction with Django projects, it is easy to find ample help to illustrate and troubleshoot database backup and restoration operations. Nevertheless, because data management needs and tasks can vary widely, Arches supports a number of data export and import features in addition to those available through PostgreSQL. The documentation below will help you understand scenarios where different approaches may be most useful. 


Graph and Business Data Background
----------------------------------

It is first important to understand the distinctions Arches makes between "graphs" and "business data". One can define custom graphs (or reuse graphs already defined by others) in Arches to model and organize data as needed (see: :ref:`Graph Designer`). The information required to define each graph (both **Resource Models** and **Branches**) is stored as records in the Arches PostgreSQL database (see :ref:`Data Model`). 

In Arches, "business data" refers to instances of records that conform to the graphs you defined. Resource instances and tile data all qualify as business data (see more :ref:`Resource Data`). Like graphs, business data are stored as records in the Arches PostgreSQL database.

Understanding the distinctions between graph and business data will help you understand which data export and import option would best meet your needs. For instance, if you simply want to backup an Arches instance "as is" so that you can restore it along with all of its graph and business data, a good approach would be to simply use the :ref:`PostgreSQL Utilities` for database backup and restoration. However, if you want to only share certain graphs between Arches instances or if you want to do some complex transformations and mass edits on business data (externally from Arches), you may want to use some of the data export and import tools provided by Arches itself (see :ref:`Arches Import and Export Utilities`).


PostgreSQL Utilities
--------------------

PostgreSQL has powerful utilities (see `Backup and Restore <https://www.postgresql.org/docs/14/backup.html>`_) to quickly export and restore databases. One can use these utilities to dump and restore Arches databases. Assuming you have an Arches project named "my_project" (and that Arches project has a database with the same name, as is the default), you can export the entire database as below:

.. code-block:: bash

    # Export your Arches project ('my_project') to PostgreSQL 
    # binary export file called 'my_project.dump'  
    pg_dump -U postgres -h localhost -F c -b my_project > my_project-v7-5-2-2024-05-11.dump

    # Alternatively, you can dump all of your PostgreSQL databases (including your Arches DB)
    # as a SQL file. The SQL file will be larger, but as a plain text file, it will be
    # somewhat more interoperable
    pg_dumpall -U postgres > my_project-v7-5-2-2024-05-11.sql


You'll need to modify the command(s) above if your PostgreSQL database is on a different host, uses a different port, or if your Arches database has a different database name. Please review PostgreSQL documentation to understand the different backup and restore options and arguments available for use.

It is generally easiest if you make a comprehensive database backup (the entire schema, records, etc.). If you need to restore a database, it is easiest to restore a database wholesale using the ``--clean`` argument.

.. code-block:: bash
    
    # Restoring a backup copy wholesale (completely replacing the my_project database).
    pg_restore --clean -U postgres -h my_project -d postgres 'my_project-v7-5-2-2024-05-11.dump'


You may encounter difficulties restoring a PostgreSQL database dump if Arches is running and connected to that database. To get around this problem, you may need to first halt active connections to the Arches database (assuming the Arches database is named "my_project") using the following SQL expression via the PostgreSQL ``psql`` console:

.. code-block:: sql

    SELECT pg_terminate_backend(pid) from pg_stat_activity where datname='my_project';


You should carefully manage your database dump files. Different versions of Arches will have different database schemas and functions. If you want to restore an Arches database from a dump file, you will need to restore it to an instance of Arches running the same version of Arches. In the example above, the export file "my_project-v7-5-2-2024-05-11.dump" is named to include the Arches version number so this can be matched if restoration is needed.


.. warning::

    If your Arches instance manages digital media files (images, videos, documents, 3D models, etc.), these files will be stored in a file system (or cloud storage service), *NOT* in the Arches PostgreSQL database. In addition to backing up the  Arches PostgreSQL database, you will also need to take additional steps to backup those files and maintain their directory structure.


Arches Import and Export Utilities
----------------------------------

While Arches provides a number of utilities to export and import data, generally speaking, :ref:`PostgreSQL Utilities` offers fast and straightforward ways to backup and restore an Arches database. However, there may be scenarios where you may need additional flexibility to manipulate Arches data. In those circumstances, you may want to use Arches data export and import features. 

1. One can enable the :ref:`Bulk Data Manager` to activate features of the Arches administrative user interface that enable bulk export and import of business data. The Bulk Data Manager is especially useful for performing mass edits, data exports, or data imports of business data. 

2. Arches provides various command line utilities to export and import both graph and business data (see :ref:`Resource Import/Export`, :ref:`Import Commands`, and :ref:`Export Commands`). 

The import and export utilities can help in cases where you may want to modify data in ways that are not easily supported by the Arches user interface. For example, you may want to make changes to some of your legacy graph data (Resource Models and or Branches). If you already have business data using those legacy graphs, you may need to first export that business data and then make your updates to the graph. From your export files, you can then import (perhaps after making modifications) the business data for use with your newly updated graphs. The import functions have data validation and integrity checks that reduce risks of corrupting data. Of course, it is still safest to use PostgreSQL utilities to backup your database at different export, modification, and import steps.



Arches UUIDs and External (or Legacy) Identifiers
-------------------------------------------------
*Forthcoming*



Use of Cloud Computing Database Services
========================================
*Forthcoming*


Automated Backups
-----------------
*Forthcoming*


Security and Permissions
------------------------
*Forthcoming*



Security and Managing Sensitive Information
===========================================
*Forthcoming*



Data Archiving (with External Repositories)
===========================================

Arches provides excellent support for active data management. However, data curation needs and expectations (particularly in the cultural heritage sector) can extend to time scales well beyond the life of a given Arches instance. Long term data archiving requires additional planning and institutional arrangements.

While data archiving is inherently challenging, Arches' emphasis on open data formats and open standards should greatly facilitate long term data preservation:

1. **Open Formats**: Open (non-proprietary) and widely used file formats can be read by a wide range of software on a wide range of operating systems. These characteristics make open formats preferred for digital preservation. Arches exports structured data in open text-based file formats (GeoJSON, JSON, and CSV). These open, text-based formats will facilitate preservation. PostgreSQL dumps (especially in the text-based SQL format) can also be archived, though these are less preferred because they would likely contain SQL operations specific to PostgreSQL and are thus less interoperable. 

2. **Open Standards**: Arches support for modeling data with ontologies (see :ref:`Ontologies in Arches`) can make data easier to understand over the long term. Such ontologies help explain and document the meaning of the graphs (resource models and branches) used in your Arches instance. Arches graphs defined using widely used and well-documented non-proprietary ontologies, especially the CIDOC-CRM, should be easier to understand by others, including future users. JSON data exports from Arches will include references to the ontologies you may use. These ontology references will make your data exports more "self-describing". This helps reduce the time and effort needed to properly document your data for wider understanding.


.. warning::

    While Arches exports structured data in open text-based file formats, Arches can also be used to manage binary data files (images, videos, 3D models, etc.). Some of those binary files may be in very specialized or proprietary formats which would represent a much greater digital preservation challenge. If you use Arches to manage files in proprietary or specialized formats, you may need to migrate these files into more widely supported (and ideally non-proprietary) formats to meet long term preservation goals.


Repository Metadata
-------------------

A key aspect of digital preservation centers on the documentation of your data. Metadata (typically expressed according to open standards such as `Dublin Core <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/>`_) helps provide some that documentation. Metadata helps to make your repository data easier to discover and easier to understand. Some metadata, particularly a copyright license (such as a `Creative Commons <https://creativecommons.org/>`_ license) also makes permissions and requirements for reuse explicit. The creation of digital repository metadata is sometimes exclusively the responsibility of the depositor. In other cases, the depositor may work with a repository's expert staff to create proper metadata. In either case, it is important to review good practices and the metadata created for related datasets to help guide your own metadata creation. Disciplinary standards and expectations, repository policies, and of course the contents of your own archiva deposits need to be considered. Professionalism, care, and awareness of community needs and expectations must inform metadata for digital preservation.


Repository Institutions and Trust
---------------------------------

Digital repositories have significant technical, expertise, and financial requirements to operate over the long term. They require a strong institutional foundation and even so, some digital repositories (even those with certifications) have failed over the years (see: `Strecker et al 2023 <https://arxiv.org/pdf/2310.06712v1>`_). `OpenAIRE documentation <https://www.openaire.eu/find-trustworthy-data-repository>`_ helps identify certifications and other characteristics useful to identify trustworthy repositories. Even though `Zenodo <https://zenodo.org/>`_ lacks certifications, OpenAIRE still lists it as a suitable repository service provider.


Additional Data Preservation Resources
--------------------------------------

* `The Archaeology Data Service (ADS) <https://archaeologydataservice.ac.uk/help-guidance/guides-to-good-practice/digital-archiving/about-these-guidelines/>`_ provides an extensive guide to good practice on archiving data (including metadata creation, file formats, and more). While these guides specifically address issues in archiving archaeological data, they can help inform data preservation planning in other areas of cultural heritage and beyond.

* `OpenAIRE <https://www.openaire.eu/data-formats-preservation-guide>`_  provides more general guidance about long term data management planning, formats for data preservation, methods to manage sensitive data, and identification of suitable digital repositories.

* `Zenodo <https://zenodo.org/>`_ is a general purpose digital repository based at the CERN laboratory. The `EAMENA <https://eamena.org/>`_ implementation of Arches integrates the Zenodo API (`see code customization <https://github.com/eamena-project/eamena-arches-dev/tree/main/dbs/database.eamena/citation>`_) to facilitate deposit of GeoJSON records (exported from Arches) into Zenodo.
