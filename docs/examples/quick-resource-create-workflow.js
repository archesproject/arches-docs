define([
    'knockout',
    'jquery',
    'arches',
    'viewmodels/workflow',
    'views/components/workflows/final-step'
], function(ko, $, arches, Workflow) {
    return ko.components.register('quick-resource-create-workflow', {
        viewModel: function(params) {
            this.componentName = 'quick-resource-create-workflow';
            this.quitUrl = "/search";
            this.stepConfig = [
                {
                    title: 'Create Historic Resource',
                    name: 'set-basic-info',  /* unique to workflow */
                    required: true,
                    workflowstepclass: 'create-project-project-name-step',
                    informationboxdata: {
                        heading: 'Create historic resource here',
                        text: 'Begin by providing the name and type of historic resource you are adding to the database.',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'resource-name', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '99417385-b8fa-11e6-84a5-026d961c88e6',
                                        nodegroup_id: '574b58a3-e747-11e6-84a6-026d961c88e6',
                                    },
                                },
                            ], 
                        },
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'resource-type', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '99417385-b8fa-11e6-84a5-026d961c88e6',
                                        nodegroup_id: '620aac67-e747-11e6-84a6-026d961c88e6',
                                    },
                                },
                            ], 
                        },
                    ]
                },
                {
                    title: 'Add Keywords',
                    name: 'add-keywords',  /* unique to workflow */
                    required: false,
                    informationboxdata: {
                        heading: 'Add a keyword',
                        text: 'Optionally add keywords to this historic resource.',
                    },
                    layoutSections: [
                        {
                            componentConfigs: [
                                {
                                    componentName: 'default-card',
                                    uniqueInstanceName: 'resource-keywords', /* unique to step */
                                    tilesManaged: 'one',
                                    parameters: {
                                        graphid: '99417385-b8fa-11e6-84a5-026d961c88e6',
                                        nodegroup_id: '3d919f0d-e747-11e6-84a6-026d961c88e6',
                                        resourceid: "['set-basic-info']['resource-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ], 
                        },
                    ],
                },
                {
                    title: 'Finish',
                    name: 'add-resource-complete',  /* unique to workflow */
                    description: 'Finish the resource creation.',
                    layoutSections: [
                        {
                            componentConfigs: [
                                { 
                                    componentName: 'final-step',
                                    uniqueInstanceName: 'create-resource-final',
                                    tilesManaged: 'none',
                                    parameters: {
                                        resourceid: "['set-basic-info']['resource-name'][0]['resourceInstanceId']",
                                    },
                                },
                            ], 
                        },
                    ],
                }
            ];
            Workflow.apply(this, [params]);
        },
        template: { require: 'text!templates/views/components/plugins/quick-resource-create-workflow.htm' }
    });
});
