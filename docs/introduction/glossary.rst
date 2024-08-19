###############
Arches Glossary
###############

The Arches project uses a number of specialized terms. The following glossary provides definitions to Arches terminology as well as links to relevant parts of the documentation relevant to different terms. 


* **Arches Designer** A user interface for facilitating database design, i.e. the creation of Resource Models. The Arches Designer consists of many different tools, such as the Graph Designer and Card Manager, each of which helps build a different facet of Resource Model creation.

* **Basemaps** Underlying map layers which include, by default, aerial imagery, streetmaps, or terrain. You can also add your own basemaps through the same process as adding overlays.

* **Branch** Branches are building blocks that aid in the creation of resource models. When you add a branch to a resource model, its contents are copied into the resource model. This allows you to further customize the resource model while leaving the original branch unaltered.

* **Business Data** In Arches, "business data" refers to instances of records that conform to the graphs you defined. Records of resource instances and tile data all qualify as business data (see more Resource Data). Like graphs, business data are stored as records in the Arches PostgreSQL database.

* **Card** Cards are used to configure the data entry representation of a branch's graph; they define how information will be collected for each nodegroup. In some cases a complex branch may have multiple cards, which will be aggregated into a card container. Cards contain widgets, and determined how the widgets are ordered in the user interface.

* **Concept** A vocabulary term that is used throughout the Arches database to define resource. A concept has a preferred label ("house") and may have any number of alternative labels ("domicile", "townhouse"). When searching your database, a search for "domicile" would automatically use the "house" concept.

* **Concept Collections** Concepts are grouped into collections. An example would be the concepts "Eastlake", "Italianate", and "Queen Anne", all of which would be grouped in an "Architectural Style" concept collection.

* **Datatype** A defined type of business data, such as a number or a date. Each node has a datatype.

* **Enterprise-level software** Computer software, such as Arches, that is designed for deployment in organizational contexts with both needs and capabilities beyond those typical of an individual person.

* **Graph** A network of nodes, connected by edges, that defines the set of attributes for either a Branch or a Resource Model. If an ontology is enforced on the graph, each node will belong to an ontological class and only certain types of edges may be used to connect them. (See :ref:`Graph Definition`)

* **Instance** a specific example of a class or category of things-e.g., my dog Cubby is an instance of the class dogs.

* **Instance, Arches** one individual implementation of Arches- i.e., the specific Arches code, configuration options, models, RDM, workflows, and data accessible.

* **Instance, Resource** an instance of an Arches resource model (see below)- e.g., Westminster Abbey is an instance of an Arches resource model for historic buildings- i.e., one particular resource.

* **Menu** Menus are groupings of cards associated with a given resource model. They allow for an organized, thematic approach to data entry.

* **Node** The smallest unit of a graph, a node will have a name and datatype. If the graph participates in an ontology, the node must also have a CRM class, and a defined relationship (edge) between it and the node upstream of it. (See :ref:`Graph Definition`)

* **Nodegroup** Within graphs, nodes are aggregated into nodegroups. An example of a nodegroup would be Name and Name Type. Edit permissions are enforced at the nodegroup level. (See :ref:`Graph Definition`)

* **Ontology** A set of rules the govern the way nodes are defined and connected in a graph. Arches comes pre-loaded with the CIDOC CRM, an ontology developed by ICOM to model cultural heritage.

* **Overlays** Static map layers that can be added to Arches. These could be historic maps, administrative boundaries, or existing map services published elsewhere.

* **Reference Data Manager (RDM)** User interface for managing all of the concepts and word lists in your Arches database.

* **Resource Layers** Map layers that are created from your Arches database. There is one resource layer for each node with datatype "geojson-feature-collection" that is stored across all resource models.

* **Resource Model** Resource Models are top-level categories for resources in your database. When creating new resources, a data entry user must decide which resource model to use, thereby defining what information is collected for the resource. The entire Arches Designer exists to facilitate the creation and customization of resource models.

* **Resource Relationships** Arches provides the ability to relate one resource to another by creating resource relationships. Resource relationships are directional and will have an associated concept, such as "contains / is contained in".

* **Resource Report** A resource’s report shows all of the saved information for a resource. Templates for reports are associated with each resource models.

* **Tile Data** Arches stores descriptive information about resource instances as tile data. Each Tile stores one instance of all of the attributes of a given NodeGroup for a given resource instance. Tile data is a type of business data stored by Arches. See :ref:`TileModel`

* **Time Wheel** A graphical interface used to support advanced time-based visualization and search of your database.

* **Widget** An input element designed to manage form input of a specific datatype. Each widget represents one node, and widgets for all nodes in a nodegroup are contained in a single card.

