###########################
Set Resource Display Names
###########################

You may find that new resources are named ``Undefined`` in your search results. This is because the **Resource Descriptor Function** has not yet been configured for your Resource Model. Follow these steps to configure it separately for each Resource Model in your database.

1. Go to Arches Designer > Resource Models (``/graph``)
2. In the list of Resource Models, follow Manage∙∙∙ > Manage Functions
3. Select the Define Resource Descriptors function to add it to the Resource Model
4. Use the tabs to configure all three different descriptor templates.

===============================
Configure a Descriptor Template
===============================

To configure a descriptor, you must first choose what card in the Resource Model holds the data you want to display. Choose this card in the dropdown, and variables corresponding to each node in that card will be added to the template, demarcated with ``< >``. Now you can rearrange these variables, delete some of them, and/or add text to customize the descriptor.

**Example:** Consider a Resource with a ``Name`` node value of **Folsom School** and ``Name Type`` node value of **Primary**.

+---------------------------+------------------------------+
| Template                  | Result                       |
+===========================+==============================+
| ``<Name>, <Name Type>``   | Folsom School, Primary       |
+---------------------------+------------------------------+
| ``Building Name: <Name>`` | Building Name: Folsom School |
+---------------------------+------------------------------+

.. important::
    After you define your descriptors, you must **Re-Index** to update all of the existing resources in your database. This could take a while, if you have a lot of resources (that's why it's best to do this step right away!).

If there are multiple instances of a given card in a Resource, the first one added will be used to create these descriptors. To manually change this, edit the Resource in question and drag the desired tile to the top of the list.

.. warning::
    Any user with read access permission to a resource will be seeing these resource descriptors wherever it shows up in search results or on the map. If a card is intended to be hidden from any group of users, it should not be used in this function.

====================
Types of Descriptors
====================

There are three different descriptors that appear through the Arches interface.

:Display Name: Shown in search results list title, and top of reports.
:Display Description: Shown in search results list description.
:Map Popup: Shown in popup that appears when a resource is clicked in the map.
