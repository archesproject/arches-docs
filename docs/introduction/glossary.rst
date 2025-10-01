###############
Arches Glossary
###############

The Arches project uses a number of specialized terms. The following glossary provides definitions to Arches terminology as well as links to relevant parts of the documentation relevant to different terms. 


Glossary
--------

The Arches project uses a number of specialized terms. The following glossary provides definitions to Arches terminology as well as links to relevant parts of the documentation relevant to different terms.

- **Arches Application**: 
  A discrete Python package that can be integrated into one or more Arches projects. Arches Applications help to reduce development and sustainability costs for customizing Arches and adding specialized features. Some Arches Applications are more comprehensive and stand-alone software to meet the data management needs of a specific community (see :ref:`Arches Applications`). Other Arches Applications, termed *Arches Extension Applications* (see :ref:`Arches Extension Applications`), describe modular software components that can be installed and reused for in multiple Arches projects.

- **Arches Designer**: 
  A user interface for facilitating database design, i.e., the creation of Resource Models. The Arches Designer consists of many different tools, such as the Graph Designer, Card Designer, and Permissions, each of which helps build a different facet of Resource Model creation. (See :ref:`Arches Designer`)

- **Arches Package**: 
  A package is an external collection of Arches data (resource models, business data, concepts, collections) and customization files (widgets, datatypes, functions, system settings) that you can load into an Arches project. (See :ref:`Understanding Packages`)

- **Basemaps**: 
  Underlying map layers which include, by default, aerial imagery, streetmaps, or terrain. You can also add your own basemaps through the same process as adding overlays.

- **Branch**: 
  Branches are building blocks that aid in the creation of resource models. When you add a branch to a resource model, its contents are copied into the resource model. This allows you to further customize the resource model while leaving the original branch unaltered. (See: :ref:`Arches Database Theory`)

- **Business Data**: 
  In Arches, "business data" refers to instances of records that conform to the graphs you defined. Records of resource instances and tile data all qualify as business data (see more Resource Data). Like graphs, business data are stored as records in the Arches PostgreSQL database.

- **Card**: 
  Cards are used to configure the data entry representation through the Arches user interface of a branch's graph; they define how information will be collected for each nodegroup. In some cases, a complex branch may have multiple cards, which will be aggregated into a card container. Cards contain widgets and determine how the widgets are ordered in the user interface. (See: :ref:`Cards Tab`)

- **CIDOC Conceptual Reference Model (CRM)**: 
  An ontology developed by the International Committee for Documentation (CIDOC) of the International Council of Museums (ICOM) to model cultural heritage information. The `CIDOC CRM <https://cidoc-crm.org/>`_ has been adopted by the International Organization for Standardization (ISO) as an international standard.

- **Concept, Arches**: 
  A vocabulary term that is used throughout the Arches database to define resources. A concept has a preferred label (e.g., "house") and may have any number of alternative labels (e.g., "domicile", "townhouse"). When searching your database, a search for "domicile" would automatically return the "house" concept. (See: :ref:`Reference Data Manager (RDM)`)

- **Concept Collections**: 
  Concepts are grouped into collections. An example would be the concepts "Craftsman," "Art Deco," and "Queen Anne," all of which would be grouped in an "Architectural Style" concept collection. (See: :ref:`Reference Data Manager (RDM)`)

- **Datatype**: 
  A defined type of business data, such as a number or a date. Each node must be assigned a datatype. (See: :ref:`Core Arches Datatypes`)

- **Edge**: 
  Edges represent the connections or relationships between nodes and can be defined by semantic properties. (See: :ref:`Edge`)

- **Enterprise-level software**: 
  Computer software, such as Arches, that is designed for deployment in organizational contexts with both needs and capabilities beyond those typical of an individual person. Enterprise software is typically installed on a physical server or through cloud-based server services.

- **Graph**: 
  A network of nodes, connected by edges, that defines the set of attributes for either a Branch or a Resource Model. If an ontology is enforced on the graph, each node will belong to an ontological class and only certain types of edges may be used to connect them. (See :ref:`Graph Definition`)

- **Helper Application (App)**: 
  A modular software components that can be installed and reused for in multiple Arches projects (see :ref:`Arches Extension Applications`)

- **Implementation, Arches**: 
  A specific deployment of Arches software that is installed, managed, and maintained by an individual, a team, or an organization. Arches implementations can be hosted on hardware owned by an individual or organization, or, alternatively, Arches implementations can run on cloud-computing services.

- **Instance**: 
  A specific example of a class or category of things, e.g., my dog Cubby is an instance of the class dogs.

- **Instance, Arches**: 
  One individual implementation of Arches, i.e., the specific Arches code, configuration options, models, RDM, workflows, and data accessible.

- **Instance, Resource**: 
  An Arches data record that expresses a particular Arches resource model (see below), e.g., the Arches data record for Westminster Abbey is a resource instance of the Arches for HERs Monument resource model.

- **Menu**: 
  Menus are groupings of Arches user interface cards associated with a given resource model. They allow for an organized, thematic approach to data entry.

- **Node**: 
  The smallest unit of a graph, a node will have a name and datatype. If the graph participates in an ontology, the node must also have an ontology class and a defined relationship (edge) between it and the node upstream of it. (See :ref:`Graph Definition`)

- **Nodegroup**: 
  Within graphs, nodes are aggregated into nodegroups. An example of a nodegroup would be the grouping of Name and Name Type. Edit permissions in Arches are enforced at the nodegroup level. (See :ref:`Graph Definition`)

- **Ontology**: 
  A set of rules that governs the way nodes are defined and connected in a graph. Arches comes pre-loaded with the CIDOC Conceptual Reference Model (CRM). (See the CIDOC CRM Entry above)

- **Overlays**: 
  Static map layers that can be added to Arches. These could be historic maps, administrative boundaries, or existing map services published elsewhere. (See :ref:`Managing Map Layers`)

- **Reference Data Manager (RDM)**: 
  User interface for managing all of the concepts and word lists in your Arches database.  (See: :ref:`Reference Data Manager (RDM)`)

- **Resource Layers Map**: 
  Geospatial layers that are created from your Arches database. There is one resource layer for each node with datatype "geojson-feature-collection" that is stored across all resource models. (See :ref:`Managing Map Layers`)

- **Resource Model**: 
  Resource Models are top-level categories for resources in your database. When creating a new resource, a data entry user must decide which resource model to use, thereby defining what information is collected for the resource. The Arches Designer provides for the creation and customization of resource models. (See: :ref:`Arches Database Theory`)

- **Resource Relationships**: 
  Arches provides the ability to create and define relationships between resources. Resource relationships can be defined by the inherited semantic property or by the label of a concept and are bi-directional.

- **Resource Report**: 
  A resource's report shows all, or a determined set, of the saved information for a resource. Templates for reports are associated with each resource model.

- **Tile Data**: 
  Arches stores descriptive information about resource instances as tile data. Each Tile stores one instance of all of the attributes of a given NodeGroup for a given resource instance. Tile data is a type of business data stored by Arches. (See :ref:`TileModel`)

- **Time Wheel**: 
  A graphical interface used to support advanced time-based visualization and search of information within your Arches database. (See :ref:`Time Wheel Configuration`)

- **Widget**: 
  A user interface input element designed to manage form input of a specific datatype. Each widget represents one node, and widgets for all nodes in a nodegroup are contained in a single card. (See :ref:`Widgets`)

- **Workflows, Arches**: 
  Workflows are a type of Plugin that can simplify the data entry process. A workflow is composed of one or more cards from a resource model, placing them in a step-through set of forms. (See :ref:`Workflows`)


