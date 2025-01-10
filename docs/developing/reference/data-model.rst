##########
Data Model
##########

.. figure:: ../../images/arches-data-model-2022-04-18.png
    :width: 100%
    :align: center

    Arches data model.

.. figure:: ../../images/full-data-model-2022-04-18.png
    :width: 100%
    :align: center

    Full model of all apps.

***********************
Resource Model Overview
***********************


Resources in an Arches database are separated into distinct Resource
Models designed to represent a kind of physical real-world resource,
such as a historic artifact or event. In the technical sense, the term
**Resource Model** refers collectively to the following user-facing
elements in Arches:

#. A Graph data structure representing a physical real-world resource,
   such as a building, a public figure, a website, an archaeological
   site, or a historic document.

#. A set of Cards to collect and display data associated with
   instances of this Resource Model.



The relationships among these components and their dependencies are
visualized below:

.. image :: ../../images/resource-model.png
   :target: _images/resource-model.png

The Arches logical model has been developed to support this modular
construction, and the relevant models are described below as they
pertain to the graph, UI components, and the resource data
itself (not illustrated above).

.. note::

   In the UI you will see a distinction between "Resource Models" and
   "Branches", but underneath these are both made from instances of the `Graph model
   <#graphmodel>`_. The primary difference between the two
   is the ``isresource`` property, which is set to ``True`` for a
   Resource Model.

   Branches are used for records that might appear in multiple
   Resource Models, such as a person or place. Branches can be
   included as children of any Ontology-permitted Node in a Resource
   Model.



***********
Controllers
***********

Arches platform code defines base classes for some of its core data
models, and uses `proxy models
<https://docs.djangoproject.com/en/stable/topics/db/models/#proxy-models>`_
to implement their controllers. In smaller classes, "controller" code
is included with the data model class. This documentation primarily
discusses the models, but controller behavior is discussed where
relevant to how the models are used, and all models are referred to by
their more succinct "controller" name.

=====================   ==================
**Model**               **Controller**
`ResourceInstance`_     `Resource <https://github.com/archesproject/arches/blob/4.3.1/arches/app/models/resource.py#L35>`_
`CardModel`_            `Card <https://github.com/archesproject/arches/blob/4.3.1/arches/app/models/card.py#L25>`_
`TileModel`_            `Tile <https://github.com/archesproject/arches/blob/4.3.1/arches/app/models/tile.py#L36>`_
`GraphModel`_           `Graph <https://github.com/archesproject/arches/blob/4.3.1/arches/app/models/graph.py#L33>`_
=====================   ==================

.. note::

   ``ResourceInstance`` breaks the implicit naming convention above
   because the term "Resource Model" refers to a specific Arches
   construct, as explained in the :ref:`Resource Model Overview` above.

****************
Graph Definition
****************

A Graph is a collection of :ref:`NodeGroups <nodegroup>`, :ref:`Nodes
<node>`, and :ref:`Edges <edge>` which connect the Nodes.

.. note::

   This definition does not include UI models and attributes, which
   are discussed :ref:`below <ui component models>`.

In the Arches data model, Nodes represent their graph data structure
namesakes, sometimes called `vertices`. A Node does the work of
defining the Graph data structure in conjunction with one or more
Edges, and sometimes collecting data.

NodeGroups are an Arches feature used to represent a group of one or
more Nodes that collect data. NodeGroups can be nested, creating a
metadata structure which is used to display the graph in the UI and
collect related information together.

A NodeGroup exists for every Node that collects data, and both
contains and shares its UUID with that node (see
:ref:`naming conventions for references <id vs id>`).  NodeGroups with more than
one member Node are used to collect composite or semantically-related
information. For example, a NodeGroup for a Node named ``Name.E1`` may
contain a ``Name Type.E55`` Node. This way, a Graph with this
NodeGroup may store Names with multiple "types", always collecting the
information together.

NodeGroups are used to create :ref:`Cards <cardmodel>`, and this is done
based on the ``cardinality`` property. Therefore, not every NodeGroup
will be used to create a Card, which allows NodeGroups to exist within
other NodeGroups. The ``parentnodegroup`` property is used to record
this nesting.

A user-defined Function may be registered and then associated with a
Graph in order to extend the behavior of Arches. For more information,
see :ref:`here <Functions>`.


GraphModel
==========

.. literalinclude:: ../../examples/arches/graphmodel.py
   :language: python

Node
====

.. literalinclude:: ../../examples/arches/node.py
   :language: python

NodeGroup
=========

.. literalinclude:: ../../examples/arches/nodegroup.py
   :language: python


Edge
====

.. literalinclude:: ../../examples/arches/edge.py
   :language: python


Function
========

.. literalinclude:: ../../examples/arches/function.py
   :language: python


**********
Ontologies
**********

An ontology standardizes a set of valid CRM (Conceptual Reference
Model) classes for Node instances, as well as a set of relationships
that will define Edge instances. Most importantly, an ontology
enforces which Edges can be used to connect which Nodes. If a
pre-loaded ontology is designated for a Graph instance, every
NodeGroup within that Graph must conform to that ontology. You
may also create an "ontology-less" graph, which will not define
specific CRM classes for the Nodes and Edges.

These rules are stored as `OntologyClass`_ instances, which are stored
as JSON. These JSON objects consist of dictionaries with two
properties, `down` and `up`, each of which contains another two
properties `ontology_property` and `ontology_classes` (`down` assumes
a known domain class, while `up` assumes a known range class).

.. code-block:: json

  {
    "down":[
      {
        "ontology_property":"P1_is_identified_by",
        "ontology_classes": [
          "E51_Contact_Point",
          "E75_Conceptual_Object_Appellation",
          "E42_Identifier",
          "E45_Address",
          "E41_Appellation"
        ]
      }
    ],
  "up":[
    {
      "ontology_property":"P1_identifies",
      "ontology_classes":[
        "E51_Contact_Point",
        "E75_Conceptual_Object_Appellation",
        "E42_Identifier"
        ]
      }
    ]
  }



Aches comes preloaded with the `CIDOC CRM
<http://www.cidoc-crm.org/>`_, an ontology created by ICOM
(International Council of Museums) to model cultural heritage
documentation. However, a developer may create and load an entirely
new ontology.


Ontology
========

.. literalinclude:: ../../examples/arches/ontology.py
   :language: python


OntologyClass
=============

.. literalinclude:: ../../examples/arches/ontologyclass.py
   :language: python

**********
RDM Models
**********

The RDM (Reference Data Manager) stores all of the vocabularies used
in your Arches installation. Whether they are simple wordlists or a
polyhierarchical thesauri, these vocabularies are stored as "concept
schemes" and can be viewed as an aggregation of one or more `concepts
<#concept>`_ and the semantic relationships (links) between those
concepts.

In the data model, a concept scheme consists of a set of Concept
instances, each paired with a `Value`_. In our running name/name_type
example, the ``Name Type.E55`` Node would be linked to a Concept
(``Name Type.E55``) which would have two child Concepts. Thus, where
the user sees a dropdown containing "Primary" and "Alternate", these
are actually the Values of ``Name Type.E55``'s two descendent
Concepts. The parent/child relationships between Concepts are stored
as `Relation`_ instances.

Concept
=======

.. literalinclude:: ../../examples/arches/concept.py
   :language: python


Relation
========

.. literalinclude:: ../../examples/arches/relation.py
   :language: python

Value
=====

.. literalinclude:: ../../examples/arches/value.py
   :language: python

*************
Resource Data
*************

Three models are used to store Arches business data:

+ ``ResourceInstance`` - one per resource in the database

+ ``Tile`` - stores all business data

+ ``ResourceXResource`` - records relationships between resource instances


Creating a new resource in the database instantiates a new
`ResourceInstance`_, which belongs to one resource model and has a
unique ``resourceinstanceid``. A resource instance may also have its
own security/permissions properties in order to allow a fine-grained
level of user-based permissions.

Once data have been captured, they are stored as Tiles in the
database. Each Tile stores one instance of all of the attributes of a
given NodeGroup for a resource instance, as referenced by the
``resourceinstanceid``. This business data is stored as a JSON object,
which is a dictionary with n number of keys/value pairs that represent
a Node's id ``nodeid`` and that Node's value.

in theory:

.. code-block:: json

   {
        "nodeid": "node value",
        "nodeid": "node value"
   }



in practice:

.. code-block:: json

   {
        "20000000-0000-0000-0000-000000000002": "John",
        "20000000-0000-0000-0000-000000000004": "Primary"
   }

(In keeping with our running example, the keys in the second example
would refer to an ``Name.E1`` node and an ``Name Type.E55`` node,
respectively.)


Arches also allows for the creation of relationships between resource
instances, and these are stored as instances of the
`ResourceXResource`_ model. The ``resourceinstanceidfrom`` and
``resourceinstanceidto`` fields create the relationship, and
``relationshiptype`` qualifies the relationship. The latter must
correspond to the appropriate top node in the RDM. This constrains the
list of available types of relationships available between resource
instances.

ResourceInstance
================

.. literalinclude:: ../../examples/arches/resourceinstance.py
   :language: python


TileModel
=========

.. literalinclude:: ../../examples/arches/tilemodel.py
   :language: python


ResourceXResource
=================

.. literalinclude:: ../../examples/arches/resourcexresource.py
   :language: python


Edit Log
==========

A change in a Tile's contents, which is the result of any resource
edits, is recorded as an instance of the EditLog model.

.. literalinclude:: ../../examples/arches/editlog.py
   :language: python

*******************
UI Component Models
*******************

A number of models exist specifically to support the resource model
UI. The purpose of this is to create direct relationships between the
resource graph and the data entry cards that are used to create
resource instances. Generally, the process works like this:

#. A resource graph is an organized collection of NodeGroups which
   define what information will be gathered for a given resource
   model.

#. A resource's :ref:`Cards <cardmodel>` and are tied to specific
   NodeGroups and define which input :ref:`Widgets <widget>` will be used
   to gather values for each Node in that NodeGroup. :ref:`Card Components
   <card component>` are used to render the cards in various contexts
   in the Arches UI.


.. image:: ../../images/graph-cards.png
   :target: _images/graph-cards.png


Cards are UI representations of a NodeGroup, and they encapsulate the
Widgets that facilitate data entry for each Node in a given NodeGroup
instance.

While a Card will only handle data entry for a single NodeGroup (which
may have many Nodes or NodeGroups), a single NodeGroup can be handled
by more than one Card.

Throughout the Arches UI, Card Components are used to render Cards in
both read-only and data entry contexts.

.. note::

   Beginning in Arches 4.3, Card Components provide functionality
   formerly provided by Forms, Menus, and Reports.


CardModel
=========

.. literalinclude:: ../../examples/arches/cardmodel.py
   :language: python


Card Component
==============

A Card Component renders a Card.

.. literalinclude:: ../../examples/arches/cardcomponent.py
   :language: python

Field description:

:name: a name to be displayed in the UI for this component
:description: a description to be displayed in the UI for this component
:component: a require path for the JS module representing this component
:componentname: a Knockout.js component name used by this component (for rendering via knockout's component binding handler)
:defaultconfig: a default JSON configuration object to be used by cards that implement this component

Widget
======

.. literalinclude:: ../../examples/arches/widget.py
   :language: python


DDataType
=========
Used to validate data entered into ``widgets``

.. literalinclude:: ../../examples/arches/ddatatype.py
   :language: python

******************
Naming Conventions
******************

``id`` vs ``_id``: ID as Primary Key vs Foreign Key
===================================================

.. Behold the irony: the actual section name starts with "id vs _id",
   but for our Sphinx reference we need to put an underscore before
   the first word of the target name, thus making it look like the
   target is reversed from the section name.  That's not actually
   what's going on, but only someone who knows both Sphinx refs and
   the naming conventions for IDs in the Arches code, or who reads
   this comment, would know that.

.. _id vs id:

Throughout the code, you will sometimes see an entity name with "id"
appended and other times see the same name with "_id" appended.  For
example, you'll see both ``nodegroupid`` and ``nodegroup_id``.

What is the difference?

The first, ``nodegroupid``, is a UUID attribute in the database and is
the primary key for entities of type NodeGroup.

The second, ``nodegroup_id``, is a foreign key attribute (thus also a
UUID) that refers from somewhere else to a NodeGroup.  For example, a
Node object may have an associated NodeGroup; that NodeGroup object
itself would be referenced as ``node.nodegroup``, and the NodeGroup's
UUID -- which in the context of a Node object is a foreign key --
would therefore be ``node.nodegroup_id``.

The reason to use ``node.nodegroup_id``, instead of getting the
NodeGroup's ID by going through the associated NodeGroup object with
``node.nodegroup.nodegroupid``, is that the latter would involve an
extra database query to fetch the NodeGroup instance, which would be a
waste if you don't actually need the NodeGroup itself.  When all you
need is the NodeGroup's UUID -- perhaps because you're just going to
pass it along to something else that only needs the UUID -- then
there's no point fetching the entire NodeGroup when you already have
the Node in hand and the Node's ``nodegroup_id`` field is a foreign
key to the Node's associated NodeGroup.  You might as well just get
that foreign key, ``node.nodegroup_id``, directly.
