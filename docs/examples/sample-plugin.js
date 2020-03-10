define([
    'jquery',
    'knockout',
    'arches'
], function($, ko, arches) {

    var SamplePlugin = function(params) {
    };

    return ko.components.register('sample-plugin', {
        viewModel: SamplePlugin,
        template: { require: 'text!templates/views/components/plugins/sample-plugin.htm' }
    });
});
