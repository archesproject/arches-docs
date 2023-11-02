################
Resource Reports
################

Arches enables projects to have custom reports on a per-resource model basis. Below is a guide to create and implement a custom resource report.

In your project, you'll need to create files in the following directories. If any directories listed here do not exist in your project, create them first.

.. code-block:: bash

        my_proj/my_proj/reports/custom_report.json
        my_proj/my_proj/media/js/reports/custom_report.js
        my_proj/my_proj/templates/views/report-templates/custom_report.htm

Sample report ``.json`` file:

.. code-block:: bash

        {
            "name": "My Custom Report Name",
            "componentid": "aee56c3a-44cf-4ab2-a5fb-6c51cda7b760",
            "component": "reports/custom_report",
            "componentname": "custom_report",
            "description": "A custom report.",
            "defaultconfig": {}
        }

Sample report ``.js`` file:

.. code-block:: bash

        define([
            'knockout',
            'viewmodels/report',
            'templates/views/report-templates/custom_report.htm'
        ], function(ko, ReportViewModel, customReportTemplate) {
            return ko.components.register('custom_report', {
                viewModel: function(params) {
                    params.configKeys = [];
                    var self = this;
                    // define params for custom report here

                    ReportViewModel.apply(this, [params]);
                    // Put custom report logic here
                },
                template: customReportTemplate,
            });
        });

Sample report ``.htm`` file (note that extending the core arches default report is optional. See core arches default report for reference on overriding specific tagged sections, e.g. "{% block header %}".):

.. code-block:: html

        {% extends "views/report-templates/default.htm" %}
        {% load i18n %}

        {% block body %}
            <!--ko if: hasProvisionalData() && (editorContext === false) -->
            <div class="report-provisional-flag">{% trans 'This resource has provisional edits (not displayed in this report) that are pending review' %}</div>
            <!--/ko-->
            <!--ko if: hasProvisionalData() && (editorContext === true && report.userisreviewer === true) -->
            <div class="report-provisional-flag">{% trans 'This resource has provisional edits (not displayed in this report) that are pending review' %}</div>
            <!--/ko-->
            <!--ko if: hasProvisionalData() && (editorContext === true && report.userisreviewer === false) -->
            <div class="report-provisional-flag">{% trans 'This resource has provisional edits that are pending review' %}</div>
            <!--/ko-->

            <div class="rp-report-section relative rp-report-section-root">
                <div class="rp-report-section-title">
                    <!-- ko foreach: { data: report.cards, as: 'card' } -->
                        <!-- ko if: !!(ko.unwrap(card.tiles).length > 0) -->
                        <!-- ko if: $index() !== 0 --><hr class="rp-tile-separator"><!-- /ko -->
                        <div class="rp-card-section">
                            <!-- ko component: {
                                name: card.model.cardComponentLookup[card.model.component_id()].componentname,
                                params: {
                                    state: 'report',
                                    preview: $parent.report.preview,
                                    card: card,
                                    pageVm: $root,
                                    hideEmptyNodes: $parent.hideEmptyNodes
                                }
                            } --> <!-- /ko -->
                        </div>
                        <!-- /ko -->
                    <!-- /ko -->
                </div>
            </div>
            {% endblock body %}

Before registering your report, ensure that named references to the various report files are consistent. For ease, it is recommended to use one single name for all files to match the component name. Check the named references in your ``.js`` file to your component as well as the template name in case you encounter issues later.

Registering your report:

.. code-block::

        (ENV) $ python manage.py report register -s ./my_proj/reports/custom_report.json

Finally, in the Arches Graph Designer interface, navigate to the "Cards" tab of the resource model this report is for, click the root/top node in the card tree (is the name of the graph/resource model) in the left-hand side. On the far-right you will see a heading "Report Configuration". Select your custom report from the dropdown labeled "Template", and save changes. 

**Troubleshooting Tips**

- Ensure that all references to a component name are consistent. 
- Ensure that references to a template (``.htm`` file) are consistent.
- Ensure your report exists in your database by checking the "report_templates" table.

**Further Interest**

Because templates often call other templates, e.g. the default report template for a resource instance in turn calls the default card component template, it may be of interest to either override or create a custom component for cards which get rendered within resource reports.

