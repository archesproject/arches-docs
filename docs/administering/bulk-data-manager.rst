#################
Bulk Data Manager
#################

As of version 7.4, Arches provides **Bulk Data Manager** user interface tools for administrators to import and update large sets of data "in bulk". These allow administrators to make changes across large sets of data, not just record by record.


----------------------------
Enable the Bulk Data Manager
----------------------------
The Bulk Data Manager is an Arches plugin (see :ref:`Plugins`). This plugin will be installed when you install Arches, but, by default, the Bulk Data Manager will be hidden.

To enable use of the Bulk Data Manager, login to the :ref:`Django Admin User Interface <django admin user interface>` and click the link to "Plugins" under models, click the "Bulk Data Manager", and edit the JSON value for the attribute "Config".

To enable use of the Bulk Data Manager the Config should be: ``{"show": true}``. To disable use of the Bulk Data Manager, the Config should be: ``{"show": false}``. Once you've made your change, press the "Save" button in the lower right.

The image below illustrates how to enable the Bulk Data Manager:

.. figure:: ../images/admin-bulk-data-manager-enable.gif
    :width: 100%
    :align: center

    Enable the Bulk Data Manager via the Django Admin panel.


.. note:: The Bulk Data Manager requires that you have properly installed and configured :ref:`Task Management` with Celery.


----------------------------
Using the Bulk Data Manager
----------------------------
Once you've enabled the Bulk Data Manager, Arches administrators will have access to Import, Edit, and Export functionality.

.. figure:: ../images/bulk-data-manager-screen.png
    :width: 100%
    :align: center

    Arches Bulk Data Manager plugin.



Import
======
The Bulk Data Manager has several **Import** related features to support the configuration and ingest of tabular organized data into Arches. These features presume familiarity with both the core Arches :ref:`Data Model` and the specific resource models and branches (see :ref:`Designing the Database`) used in your instance.

The Bulk Data Manager import tools support imports of data stored in CSV and Excel files. The CSV and Excel importers require that data in tables (and in the case of Excel, worksheets) will be organized according to map properly to your resource models and node structures for these resource models. To assist in creating data properly structured for successful import, you can download an Excel workbook template for a given resource model. The animation below illustrates how to export a template for an example resource model.

.. figure:: ../images/bulk-data-manager-export-template.gif
    :width: 100%
    :align: center

    Bulk Data Manager export of an Excel template for the (example) "Collection or Set" resource model


To describe how to use the Bulk Data Manager to import data, we'll refer to the `Arches for Science <https://www.archesproject.org/arches-for-science/>`_ project *Collection or Set* resource model as an illustrative example. In the :ref:`Arches Designer`, the card for the *Name of Collection* branch of the *Collection or Set* resource model looks like this:

.. figure:: ../images/arches-designer-afs-collection-or-set-name-branch.png
    :width: 100%
    :align: center

    Arches Designer view of the *Name of Collection* card used in the *Collection or Set* resource model

If you used the Bulk Data Manager to download an Excel template file for this *Collection or Set* resource model, you would see worksheets for each branch used with the resource model. The *Name of Collection* branch of the *Collection or Set* resource model has shaded nodegroups and nodes that looks like this:

.. figure:: ../images/bulk-data-manager-excel-template-collection-or-set-name.png
    :width: 100%
    :align: center

    Excel template worksheet for *Collection or Set* resource model *Name of Collection* branch nodegroups and nodes.

The Excel template file also includes a worksheet called "metadata". The metadata worksheet describes the datatypes (see more: :ref:`Core Arches Datatypes`) expected by each node:

.. figure:: ../images/bulk-data-manager-excel-template-collection-or-set-metadata.png
    :width: 100%
    :align: center

    Excel template *metadata* worksheet for datatypes used by *Collection or Set* branch nodes.


Edit
====

The **Edit** tab of the Bulk Data Manager enables Arches administrators to make mass edits of string data across many resource instances. 
As of version 7.5.0, the current string editing options include:

1. Bulk Deletion
2. Change case (uppercase, lowercase, capitalize)
3. Replace Text
4. Remove Whitespace

.. figure:: ../images/bulk-data-editor.png
    :width: 100%
    :align: center

Editing operations require all or some of the following options:

1. Seach Url (optional) - Defines the bounds of what resources can be edited.  Actual edited resources could be less then what the search defines (`see below <search url details>`_).
2. Resource Model - Resource instances of the model to edit
3. Node - The node value in each resource instance to edit
4. Nodegroup - (Deletion only) the tile associated with the nodegroup to delete
5. Language - The language to update in each node
6. From and To - (Replace Text only) the text you would like to search and replace

.. _search url details:
    Copy and paste a URL of a search that retrieves a set of resource instances that you want to limit your bulk edit operation to.
    This does not mean that those resources will actually be edited, only that resources that don't fall within that search result won't be edited.

    For example, in a capitalize operation:
    - If a search url returns 3 records but one of them is already capitalized then only 2 records will be updated.
    - If a search url returns 3 records but the node in the model contains more then 3 records that are uncapitalized, 
    then only the 3 records defined in your search will be updated.

.. figure:: ../images/bulk-data-editor-preview.png
    :width: 100%
    :align: center

Preview button- Once you're satisfied with the options you've selected click the preview button to preview a 
small set of records that match your criteria to see the before and after of the edit operation.

Start button - Click the start button if you'd like to actually kick off the edit operation.  You will be taken to the Task Status tab. 
Depending on the operation selected and the number of resources being edited, this can take some time.
Edit operations are placed into a work queue and at this point you can leave this page.  The Task Status
will update itself every 5 seconds (there is no need to refresh the page).

