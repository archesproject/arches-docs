##############################
Creating and Editing Resources
##############################

````````````````````````````
Resource Manager
````````````````````````````

You may create new Resources only if you have access to the Resource Manager page. From there, you will begin by choosing which Resource Model you would like to use. Note that a Resource Model must have its status set to **active** for it to appear in the Resource Manager.

.. figure:: ../images/Resource-Manager.png

    Your Resource Manager page may look different than this image, depending on what Resource Models you have set up in your database.

````````````````````````````
Resource Editor
````````````````````````````

The Resource Editor is used to create new or edit existing Resources. On the left-hand side of the page you will see this Resource's "card tree", which shows all of the data entry cards that you can edit. Think of "creating data" as "adding cards".

To begin, select a card, enter data, and click Add. Some cards may allow multiple instances, in which case you will be able to add as many of the same type as you want.

.. figure:: ../images/edit-resource-simple-card.gif

   Simple data entry in Arches.

Once you have saved data for a resource, you can see a full summary by selecting the top card. This is the resource report.

In some cases, cards will be nested within other cards, as in the example of adding a geo-location below.

.. figure:: ../images/edit-resource-nested-card.gif

   Created nested data in Arches.

Provisional Edits
-----------------

If you are a member of the Resource Editor group, all of your edits--either creating new resources or editing existing ones--will be considered "Provisional". A member of the Resource Reviewer group can then approve your edits, making them "Authoritative".

1. Resource Editor makes an edit:

    .. image:: ../images/prov-edits-submitted.png

2. For Resource Reviewers, search results indicate provisional data:

    .. image:: ../images/prov-edits-search-result.png

    `Resource Editors only see provisional data while using the resource editor.`

3. Resource Reviewer will be prompted to Q/A the edit:

    .. image:: ../images/prov-edits-qa-prompt.png

4. Accept or Decline:

    .. image:: ../images/prov-edits-qa-dialog.png

5. Approved edits are immediately visible:

    .. image:: ../images/prov-edits-final.png

.. tip:: A Resource Reviewer can also use the "Q/A Type" search filter (see images above) to only find resources with (or without) provisional edits.


````````````````````````````
Related Resources
````````````````````````````

.. warning::

    Managing generic relationships as described below is still an available feature in Arches. However, **this feature will soon be deprecated** in a future release.
    Users are strongly encouraged to use the `resource-instance` datatype to manage relationships between resource instances.
    The ability to visualize connections across `resource-instance` datatype nodes will accompany the deprecation of the generic resource relationship.

From the Resource Editor you can also access the Related Resources Editor, which is used to create a relationship between this resource and another in your databas. To do so, open the editor, find the resource, and click Add. Your Resource Model will need to be configured to allow relations with the target Resource Model. If relations are not allowed, resources in the dropdown menu will not be selectable.

After a relation has been created, you can further refine its properties, such as what type of relation it is, how long it lasted, etc. While viewing the relation in grid mode, begin by selecting the relation in the table. You will see the "Delete Selected" button appear. Next click "relation properties", enter the information, and don't forget to "Save" when finished.

.. figure:: ../images/create-resource-relation.gif

    Creating a relationship between two resource in Arches, and adding properties to that relationship.

.. note:: Creating a relationship between two resources using the related resource editor is fundamentally different from creating a resource instance node in graph. Creating a relationship is good for making a visual "web" of resource relationships. Using a resource instance node in a Resource Model's graph allows you to "embed" one resource inside of another.
