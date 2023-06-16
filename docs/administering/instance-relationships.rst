========================================================
Graph Design, Instance Relationships, and Concept Labels
========================================================

Arches v7.4.0 introduced features to enable administrators to define a wider range of relationship types between resources instances. Prior to v7.4.0, relationship types could only be defined in the resource instance widget using ontology properties. Arches v7.4.0 enables users to define relationships using concept values from concept collections managed in the :ref:`Reference Data Manager (RDM)` .

*************************************************************
Steps to Make Custom Relationships between Resource Instances
*************************************************************
You will need administrative privileges to use the RDM and edit resource models and branches. If you have such permissions, the following steps enable customization of relationships between resource instances:

    1) Create and define custom relationship concepts
        In the RDM Thesauri tab, navigate to and then select the *"Arches" > "Resource To Resource Relationship Types"* concept. Under the blue "Manage" option button (right side of the screen), select *"Add Child"*. Fill out the *"Add Concept"* form to describe your new custom resource to resource relationship type. If the direction of your custom relationship matters, you should also define an inverse relationship. For example, the inverse of "contains" can be "is contained by".

        .. image:: ../images/resource-to-resource-rel-create-contained.gif

    2) Add custom relationship concept to dropdown entry
        In the RDM Collections tab, navigate to and then select the *"Resource To Resource Relationship Types"* collection (it has the same name as the concept). Click the *"Add dropdown entry"* text, and this will open a dialogue where you can find and select your custom relationship concept to add to the *"Resource To Resource Relationship Types"* collection. This step makes your custom relationship available for use when you edit or create resource instances.

        .. image:: ../images/resource-to-resource-rel-add-dropdown-contained.gif

    3) Use your custom resource to resource relationship concept in a branch
        After you finish creating custom relationships (and their inverse relations), you can now use the Arches Designer to implement the custom relationships in your resource models. To use your custom resource to resource relationships, create a branch where the "Root Node Data Type" is either a "resource-instance" or a "resource-instance-list". Once you select a resource model for use with this branch, click on the resource model label. This will open a form that will allow you to select a custom resource to resource relationship and the inverse of that relationship. After you save and publish, you will be able to use the custom resource to resource relationships as you create and edit resource instances.

        .. image:: ../images/resource-to-resource-rel-add-to-branch.gif
