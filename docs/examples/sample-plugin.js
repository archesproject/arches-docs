define([
    'jquery',
    'knockout',
    'arches',
    'templates/views/components/plugins/sample-plugin.htm',
], function($, ko, arches, samplePluginTemplate) {

    var SamplePlugin = function(params) {
    };

    return ko.components.register('sample-plugin', {
        viewModel: SamplePlugin,
        template: samplePluginTemplate,
    });
});
