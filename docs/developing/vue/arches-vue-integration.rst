Arches Vue Integration Guide
============================

This guide explains how to embed a Vue 3 application into Arches using the
``createVueApplication`` helper. This function bootstraps your app with:

- Arches i18n (via vue3-gettext)  
- PrimeVue + default theme  
- Common services (confirmation, dialogs, toasts)  
- Shared directives (tooltips, focus trap, scroll animations)  
- Automatic dark-mode theme switching

Supported Use Cases
~~~~~~~~~~~~~~~~~~~

- **Full-page views** (reports, dashboards)  
- **Standalone plugins**  
- **Knockout-embedded components**  

Not yet supported: Arches “widgets” that require specialized render context.

Quick Start
~~~~~~~~~~~

1. **Import** your root component and the helper:

   .. code-block:: js

       import createVueApplication from 'utils/create-vue-application'
       import MyVueApp from '@/my_project/MyVueApp.vue'

2. **Initialize** and **mount**:

   .. code-block:: js

       createVueApplication(MyVueApp)
            .then(app => {
                // Optional: register extra plugins or globalProperties here
                app.mount('#my-vue-mount-point');
            })
            .catch(err => {
                console.error('Vue integration failed:', err);
            })

3. **Ensure** your Arches template contains the mount point:

   .. code-block:: html

       <!-- In your Django/Knockout template -->
       <div id="my-vue-mount-point"></div>

Knockout Integration Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: js

    // src/my_project/MyPlugin.vue

    <script setup lang="ts">
    import { onMounted } from 'vue';
    import { useGettext } from 'vue3-gettext';

    const { $gettext } = useGettext();

    onMounted(() => {
        console.log($gettext('Hello from the <script> tag!'));
    });
    </script>

    <template>
        <h1 class="header">
            {{ $gettext("Hello from the template!") }}
        </h1>
    </template>

    <style scoped>
    .header {
        color: red;
    }
    </style>

.. code-block:: js

    // media/js/views/components/plugins/my-plugin.js

    import ko from 'knockout';
    import createVueApplication from 'utils/create-vue-application';
    import MyPlugin from '@/my_project/MyPlugin.vue';
    import template from 'templates/views/components/plugins/my-plugin.htm';

    ko.components.register('my-plugin', {
        viewModel: function() {
            createVueApplication(MyPlugin)
                .then(vueApp => vueApp.mount('#my-plugin-mount'))
                .catch(console.error)
        },
        template: template
    });

.. code-block:: html

    <!-- templates/views/components/plugins.htm -->
    
    <div id="my-plugin-mount"></div>