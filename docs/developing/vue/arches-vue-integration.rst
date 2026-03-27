############################
Arches Vue Integration Guide
############################

This guide explains how to embed a Vue 3 application into Arches using the
``createVueApplication`` helper. This function bootstraps your app with:

- Arches frontend internationalization (i18n) via vue3-gettext
- PrimeVue + default theme
- Common services (confirmation, dialogs, toasts)
- Shared directives (tooltips, focus trap, scroll animations)
- Automatic dark-mode theme switching

Supported Use Cases
===================

- **Full-page views** (reports, dashboards)
- **Standalone plugins**
- **Knockout-embedded components**

Not yet supported: Arches "widgets" that require specialized render context.

Frontend Agnosticism
====================

Arches Vue applications should be **fully decoupled from the Django/Knockout layer**.
In almost all cases, Vue components should not receive data from Django template context,
Knockout observables, or other server-rendered state. All data should be fetched by
the Vue application itself via API calls.

Keeping the frontend agnostic means:

- **Portability**: components can be developed, tested, and reused without a Django process.
- **Predictability**: all state has a single origin — the Vue app itself — eliminating hidden data dependencies.
- **Maintainability**: the boundary between the server and client stays clean and explicit.

As a general rule, avoid:

- Data attributes on mount points
- Global JavaScript variables set by Django templates
- Knockout observable bindings passed into Vue
- ``initialProps`` via ``createVueApplication`` (see :ref:`createvueapplication-api`)

``initialProps`` exists as an escape hatch for cases where bootstrapping truly requires
server-provided data and a fetch round-trip is not feasible.
Use it sparingly and document the reason clearly when you do.

Quick Start
===========

1. **Import** your root component and the helper:

   .. code-block:: js

       import createVueApplication from 'utils/create-vue-application';
       import MyVueApp from '@/my_project/MyVueApp.vue';

2. **Initialize** and **mount**:

   .. code-block:: js

       createVueApplication(MyVueApp)
            .then(app => {
                // Optional: register extra plugins or globalProperties here
                app.mount('#my-vue-mount-point');
            })
            .catch(err => {
                console.error('Vue integration failed:', err);
            });

3. **Ensure** your Arches template contains the mount point:

   .. code-block:: html

       <!-- In your Django/Knockout template -->
       <div id="my-vue-mount-point"></div>

Knockout Integration Example
============================

A Knockout-embedded Vue component requires three files: a Vue SFC, a Knockout
component wrapper, and an HTML template.

**1. The Vue SFC** (``src/my_project/MyPlugin.vue``):

.. code-block:: vue

    <script setup lang="ts">
    import { useGettext } from 'vue3-gettext';

    const { $gettext } = useGettext();
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

**2. The Knockout wrapper** (``media/js/views/components/plugins/my-plugin.js``):

.. code-block:: js

    import ko from 'knockout';
    import createVueApplication from 'utils/create-vue-application';
    import MyPlugin from '@/my_project/MyPlugin.vue';
    import template from 'templates/views/components/plugins/my-plugin.htm';

    ko.components.register('my-plugin', {
        viewModel: function() {
            createVueApplication(MyPlugin)
                .then(vueApp => vueApp.mount('#my-plugin-mount'))
                .catch(console.error);
        },
        template: template
    });

**3. The HTML template** (``templates/views/components/plugins/my-plugin.htm``):

.. code-block:: html

    <div id="my-plugin-mount"></div>

URL Generation
==============

All API request URLs must be generated using ``generateArchesURL`` from
``@/arches/utils/generate-arches-url.ts``. Never hardcode URL strings.

.. code-block:: js

    generateArchesURL(urlName, urlParameters?, languageCode?, queryArgs?)

Returns a URL string resolved against the globally registered ``ARCHES_URLS``
object, which Django generates at runtime.

**Parameters**

- ``urlName`` *(required)* — The namespaced Django URL name (e.g. ``'my_app:my_view'``).
- ``urlParameters`` *(optional)* — Path parameters to interpolate into the URL (e.g. ``{ id: resourceId }``).
- ``languageCode`` *(optional)* — Override the language code. Defaults to ``document.documentElement.lang``.
- ``queryArgs`` *(optional)* — Key/value pairs to append as a query string.

.. code-block:: js

    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    // Simple URL
    const url = generateArchesURL('my_app:resources');
    // → /en/resources

    // With path parameters
    const url = generateArchesURL('my_app:resource-detail', { id: resourceId });
    // → /en/resources/abc123

    // With query args
    const url = generateArchesURL('my_app:resources', {}, undefined, { page: 1, limit: 10 });
    // → /en/resources?page=1&limit=10

**Why?**

- **Language awareness**: URLs are automatically prefixed with the active language code.
- **No hardcoding**: URL patterns are defined once in Django and consumed in the frontend without duplication.
- **Type safety**: Parameters are typed as ``string | number``, preventing malformed URLs.

.. _createvueapplication-api:

``createVueApplication`` API
============================

.. code-block:: js

    createVueApplication(vueComponent, themeConfiguration?, initialProps?)

Returns a ``Promise<App>`` — a Vue application instance ready to be mounted.

**Parameters**

- ``vueComponent`` *(required)* — The root Vue SFC to bootstrap.
- ``themeConfiguration`` *(optional)* — A PrimeVue theme preset. Defaults to
  ``DEFAULT_THEME`` from ``@/arches/themes/default.ts``. Override this to apply
  a custom theme to your application.
- ``initialProps`` *(optional, avoid)* — Avoid passing props from the Django/Knockout
  layer. All application state should originate inside Vue. See `Frontend Agnosticism`_.

The returned ``app`` instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before calling ``.mount()``, you can register additional plugins or set global
properties on the returned app:

.. code-block:: js

    createVueApplication(MyVueApp)
        .then(app => {
            app.use(MyPlugin);
            app.config.globalProperties.$myUtil = myUtil;
            app.mount('#my-vue-mount-point');
        })
        .catch(console.error);
