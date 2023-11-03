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
The **Edit** tab of the Bulk Data Manager enables Arches administrators to make mass edits of string data across many resource instances. As of version 7.4.0, the current string editing options include:

1. Change classes
2. Replace Text
3. Remove Whitespace

Each editing option can be applied to selected node and languages within selected resource instances. The editing interface provides multiple options for selecting resource instances to update with a bulk edit. These options include:

1. Use search url
    One can copy and paste a URL of a search that retrieves a set of resource instances you want to edit

2. Select a resource model
    Use the dropdown list to select a resource model with resource instances that you want to edit

Use the other drop down lists to select nodes for editing, change the "From" and "To" text (if you are doing a "Replace Text" edit), and get a preview of how your edit would look. To actually make the edit, press the Start button. This may take some time, especially if you are updating many resource instances. Updates also trigger re-indexing, which can also take some time.
