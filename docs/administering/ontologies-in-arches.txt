####################
Ontologies in Arches
####################

Arches data is modeled with graphs. A graph is a collection of nodes, structured like branches, all emanating from the
root node, which represents the resource itself. If you are modeling a building resource, you may have a root node
called "Building" with a node attached to it called "Name". You can imagine that complex and thoroughly documented
resources will have many, many nodes.

An ontology is a set of rules that categorizes these nodes into classes, and dictates which classes can be connected to
each other. It's a "rulebook" for graph construction.

For many Arches applications data modelers will want to use a CRM (Conceptual Reference Model).
The CIDOC CRM v6.2 is an ontology created by ICOM specifically to describe cultural heritage data. To learn more about
the CIDOC CRM, visit `cidoc-crm.org <http://www.cidoc-crm.org/>`_ or view a `full list of classes and
properties <http://www.cidoc-crm.org/Version/version-6.2>`_.

Loading an Ontology
-------------------

Arches no longer comes preloaded with the CIDOC CRM, but it's simple to load it or any other ontology. To load the CRM
just download or clone it from this repository: https://github.com/archesproject/cidoc-crm-ontology. `download <https://github.com/archesproject/cidoc-crm-ontology/archive/master.zip>`_

If you are developing an Arches package, you can simply unzip the downloaded zip file, and add the cidoc_crm folder to
your packages ontologies directory. When you load your package, the CIDOC CRM will load with it::

    /my_package/
    └─ ontologies
        └─ cidoc_crm


If you are not loading a package, you can unzip the downloaded file, and then run the following command with your
virtual environment activated:

.. code-block:: bash

    python manage.py load_ontology -s cidoc_crm


Loading a custom ontology
-------------------------

If you have created your own ontology or have a different version of the CIDOC CRM, then just add
your files to a folder and include an `ontology_config.json` file which contains the metadata for your ontology. Here's
and example:

.. code-block:: javascript

    {
      "base": "cidoc_crm_v6.2.xml",
      "base_name": "CIDOC CRM v6.2",
      "extensions": [
          "CRMsci_v1.2.3.rdfs.xml",
          "CRMarchaeo_v1.4.rdfs.xml",
          "CRMgeo_v1.2.rdfs.xml",
          "CRMdig_v3.2.1.rdfs.xml",
          "CRMinf_v0.7.rdfs.xml",
          "arches_crm_enhancements.xml"
      ],
      "base_version": "6.2",
      "base_id": "e6e8db47-2ccf-11e6-927e-b8f6b115d7dd"
    }

You will need to generate a UUID to use as the base_id. Do not use the one in the example above.

Enforcing ontology rules
------------------------

When creating Resource Models and Branches, users have the option of enforcing an ontology throughout the graph, or
creating a graph with no ontology. If an ontology is chosen, the Graph Designer will enforce all of the applicable node
class (CRM Entities) and edge (CRM Properties) rules during use of the Graph Designer. Importantly, if a Resource Model
uses an ontology one can only add Branches to it that have been made with the same ontology.
