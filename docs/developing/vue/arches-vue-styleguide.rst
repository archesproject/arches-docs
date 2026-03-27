######################
Arches Vue Style Guide
######################

Table of Contents
=================

- `Purpose`_
- `Basis for Style Guide`_
- `Contributions`_
- `Project Directory Structure & Naming`_
    - `File and Folder Naming Conventions`_
    - `Top-Level Structure`_
    - `Component Folder Hierarchy`_
- `Component Structure`_
    - `Single-File Components`_
    - `Component Decomposition`_
    - `Slots`_
- `Data Flow & State`_
    - `Fetch Proximity`_
    - `Primitives First`_
    - `Derived State`_
    - `Event Emission`_
- `The <script> Tag`_
    - `Coding Standards`_
    - `Import Pathing`_
    - `Import Order`_
    - `Declaration Order`_
- `The <template> Tag`_
    - `Attribute Ordering & Formatting`_
    - `Self-Closing Tags`_
    - `Logic in Templates`_
    - `Text in Templates`_
- `The <style> Tag`_
    - `Scope`_
    - `Layout Patterns`_
    - `Units & Sizing`_
    - `Offsets & Positioning`_
    - `No calc()`_
    - `Theming & Colors`_
    - `Selector Naming`_
- `Testing`_
    - `Test Location & Naming`_
    - `Writing Frontend Tests`_
    - `Running Frontend Tests`_

Purpose
=======

The purpose of this style guide is to establish a unified coding style and set of conventions that all contributors should adhere to when writing code for Arches. By following these guidelines, we aim to:

- Improve code readability and maintainability
- Facilitate collaboration among developers
- Enhance the overall quality and consistency of Arches software, Arches projects, and Arches applications

Basis for Style Guide
=====================

This style guide for Arches is built on top of the standard Vue.js and TypeScript style guides. As such, it inherits and extends the conventions and best practices outlined in those guides. Any coding style, formatting, or conventions not explicitly covered in this document should be referenced from the official Vue.js and TypeScript style guides. It's important to maintain consistency with these standard guidelines to ensure compatibility and familiarity for developers working with Vue.js and TypeScript projects.

- For Vue.js, you can refer to the `official Vue style guide <https://vuejs.org/style-guide/>`_. 
- For TypeScript, you can refer to the `Google TypeScript Style Guide <https://google.github.io/styleguide/tsguide.html>`_.

Contributions
=============

This style guide is a living document that evolves over time. We welcome contributions from the community to improve and expand this guide further. If you have suggestions, feedback, or would like to contribute to the style guide, please reach out to us via the `Arches Forum <https://community.archesproject.org/>`_.

Project Directory Structure & Naming
=====================================

File and Folder Naming Conventions
----------------------------------

**Arches entity directories** — Plural, lowercase names that reflect domain concepts (e.g. ``cards/``, ``widgets/``, ``reports/``).

**Vue component directories** — One folder per component, named in PascalCase (e.g. ``CustomComponent/``).

**Non-Vue component directories** — Utility or helper folders in kebab-case (e.g. ``custom-utility/``, ``date-utils/``).

**Vue components** — PascalCase filenames with a ``.vue`` extension (e.g. ``UserCard.vue``, ``MapViewer.vue``).

**Utilities & helpers** — kebab-case with a ``.js`` or ``.ts`` extension (e.g. ``fetch-api.ts``, ``format-date.js``).

**Type files** — Single-purpose type definitions in kebab-case ``.ts`` (e.g. ``user-profile.ts``, ``map-types.ts``).

Top-Level Structure
-------------------

Top-level directories **must** align with Arches concepts (e.g. cards, widgets, reports) when such delineation is required. Otherwise, consolidate everything under a single app-level directory.

.. code-block:: shell

    src/
    └── project_name/
        ├── plugins/
        ├── reports/
        │   └── CustomReport/
        │       ├── components/
        │       └── CustomReport.vue
        ├── widgets/
        ├── types/
        └── utils.ts

.. code-block:: shell

    src/
    └── project_name/
        ├── components/
        │   └── CustomComponent.vue
        ├── CustomApplication.vue
        ├── types/
        └── utils.ts

**Why?**

- **Standardization**: Consistent naming and structure make it easier for developers to navigate the codebase.
- **Organization**: Grouping related components together makes it easier to find and manage them.

Component Folder Hierarchy
--------------------------

At every level of the hierarchy:

- **Component files with sub-components** must reside in a folder named after the component.
- **Dependent components** must live in a ``components/`` subdirectory within their parent component's folder.
- **Shared components** (used by more than one parent) must be elevated to the ``components/`` directory at the level of the highest parent component that uses them.

.. code-block:: shell

    src/
    └── project_name/
        ├── CustomApplication.vue
        └── components/
            └── CustomDashboard/
                ├── CustomDashboard.vue
                └── components/
                    └── DashboardTable/
                        ├── DashboardTable.vue
                        └── components/
                            ├── CustomHeader.vue
                            ├── TableSection.vue
                            └── UpdatedFooter.vue

**Why?**

- **Clarity**: Each component's folder contains everything it needs, making it easier to understand and navigate.
- **Encapsulation**: Keeps related components together, reducing the risk of naming conflicts and improving modularity.

Component Structure
===================

Single-File Components
----------------------

Single-File Components (SFCs) are the preferred way to define Vue components.

.. code-block:: vue

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

**Why?**

- **Encapsulation**: All component-related code is in one place, making it easier to understand and maintain.
- **Separation of concerns**: Each section (template, script, style) has its own purpose, improving readability.

Component Decomposition
-----------------------

Components should be decomposed into smaller, reusable components whenever possible. Aim for a single responsibility per component.

.. code-block:: vue

    <!-- Bad: one component handling both edit and view concerns -->

    <script setup lang="ts">
    import { ref } from 'vue';

    import { useGettext } from 'vue3-gettext';

    import type { WidgetDisplayMode } from '@/project_name/types.ts';

    const WIDGET_UPDATE_EVENT = 'update' as const;
    const DISPLAY_MODE_EDIT = 'edit' as const;

    const { displayMode, widgetValue } = defineProps<{
        displayMode: WidgetDisplayMode;
        widgetValue: string;
    }>();

    const emit = defineEmits<{
        (event: typeof WIDGET_UPDATE_EVENT, widgetValue: string): void;
    }>();

    const { $gettext } = useGettext();

    const draftWidgetValue = ref(widgetValue);
    </script>

    <template>
        <div
            v-if="displayMode === DISPLAY_MODE_EDIT"
            class="custom-widget-editor"
        >
            <input
                v-model="draftWidgetValue"
                class="custom-widget-editor__input"
            />
            <button @click="emit(WIDGET_UPDATE_EVENT, draftWidgetValue)">{{ $gettext('Save') }}</button>
        </div>
        <div
            v-else
            class="custom-widget-viewer"
        >
            <span class="custom-widget-viewer__value">{{ widgetValue }}</span>
        </div>
    </template>

.. code-block:: vue

    <!-- Good: CustomWidget.vue delegates to single-responsibility children -->
    
    <script setup lang="ts">
    import CustomWidgetEditor from '@/project_name/widgets/CustomWidget/components/CustomWidgetEditor.vue';
    import CustomWidgetViewer from '@/project_name/widgets/CustomWidget/components/CustomWidgetViewer.vue';

    import type { WidgetDisplayMode } from '@/project_name/types.ts';

    const WIDGET_UPDATE_EVENT = 'update' as const;
    const DISPLAY_MODE_EDIT = 'edit' as const;

    const { displayMode, widgetValue } = defineProps<{
        displayMode: WidgetDisplayMode;
        widgetValue: string;
    }>();

    const emit = defineEmits<{
        (event: typeof WIDGET_UPDATE_EVENT, widgetValue: string): void;
    }>();
    </script>

    <template>
        <CustomWidgetEditor
            v-if="displayMode === DISPLAY_MODE_EDIT"
            :widget-value="widgetValue"
            @update="emit(WIDGET_UPDATE_EVENT, $event)"
        />
        <CustomWidgetViewer
            v-else
            :widget-value="widgetValue"
        />
    </template>

**Why?**

- **Reusability**: Smaller components can be reused in different contexts, reducing code duplication.
- **Maintainability**: Easier to understand and modify smaller components than large monolithic ones.
- **Testing**: Smaller components are easier to test in isolation.

Slots
-----

Use scoped slots when the consumer needs access to slot data; use regular named slots for simple content projection. Name slots clearly to indicate their purpose.

.. code-block:: vue

    <template>
        <MyTable>
            <!-- Can also use shorthand #header -->
            <template v-slot:header>
                {{ $gettext('Table Header') }}
            </template>

            <!-- Can also use shorthand #row="{ row }" -->
            <template v-slot:row="{ row }">
                <MyRow :data="row" />
            </template>
        </MyTable>
    </template>

**Why?**

- **Flexibility**: Consumers can customize the rendering of specific parts of the component.
- **Separation of concerns**: Slots allow for a clear distinction between the component's structure and its content.

Data Flow & State
=================

Use the simplest mechanism that meets your needs. In order of increasing complexity:

1. **Props & emits** — The default. For parent-child data flow when the component tree is shallow and the data is local to a subtree.

2. **provide/inject** — For sharing state across a deep component tree without prop drilling. The providing component owns and controls the state; injecting components consume it read-only.

3. **Composables** — For shared data-fetching logic or reactive utilities needed by multiple unrelated components. Each call site gets its own reactive instance unless the composable explicitly exports a shared singleton.

4. **Pinia** — For state that must be shared globally across unrelated component trees, persist across navigation, or be accessed outside of a Vue component context. Use sparingly — most Arches application state does not require a global store.

.. code-block:: vue

    <!-- 1. Props & emits: a tile viewer receives its data from a parent -->

    <TileViewer
        :tile-id="activeTileId"
        @tile-saved="onTileSaved"
    />

.. code-block:: vue

    <!-- 2. provide/inject: a resource form provides its ID to deeply nested tile editors,
         avoiding threading resourceId through every intermediate layout component -->

    <!-- ResourceForm.vue -->
    <script setup lang="ts">
    import { provide, toRef } from 'vue';

    const { resourceId } = defineProps<{ resourceId: string }>();
    provide('resourceId', toRef(() => resourceId));
    </script>

    <!-- TileEditor.vue (several levels deep) -->
    <script setup lang="ts">
    import { inject, type Ref } from 'vue';

    const resourceId = inject<Ref<string>>('resourceId')!;
    </script>

.. code-block:: typescript

    // 3. Composable: shared fetch logic — each component that calls useNodegroupData()
    //    gets its own reactive instance independently tracking its own nodegroup

    // use-nodegroup-data.ts
    import { ref, watchEffect, type Ref } from 'vue';

    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    import type { Nodegroup } from '@/project_name/types.ts';

    export function useNodegroupData(nodegroupId: Ref<string>) {
        const nodegroup = ref<Nodegroup | null>(null);
        watchEffect(async () => {
            const response = await fetch(
                generateArchesURL('arches:nodegroup', { id: nodegroupId.value })
            );
            nodegroup.value = await response.json();
        });
        return { nodegroup };
    }

.. code-block:: typescript

    // 4. Pinia: the authenticated user is global state — it must be accessible from
    //    unrelated trees (nav bar, permission checks, audit logging) and persist
    //    across navigation, making it the one case that genuinely warrants a store

    // stores/auth-store.ts
    import { ref } from 'vue';

    import { defineStore } from 'pinia';

    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    import type { AuthUser } from '@/arches/types.ts';

    export const useAuthStore = defineStore('auth', () => {
        const currentUser = ref<AuthUser | null>(null);
        async function fetchCurrentUser() {
            const response = await fetch(generateArchesURL('arches:me'));
            currentUser.value = await response.json();
        }
        return { currentUser, fetchCurrentUser };
    });

**Why?**

- **Simplicity**: Props are explicit and traceable; escalate only when the complexity genuinely requires it.
- **Encapsulation**: Each mechanism has a defined ownership model — props flow down, events flow up, provide/inject scopes to a tree, Pinia is global.
- **Testability**: Simpler mechanisms are easier to test; Pinia stores and composables can both be tested independently of components.

Fetch Proximity
---------------

Fetch data as close to the consumer as possible. Don't lift network calls higher than needed. When multiple components need the same data, extract the fetch logic into a shared composable. When state must be shared globally across unrelated component trees, use Pinia. See `Data Flow & State`_ for guidance on choosing the right mechanism.

.. code-block:: vue

    <!-- Bad: fetching at a high-level parent when only the table needs it -->

    <script setup lang="ts">
    import { ref, watchEffect } from 'vue';

    import ResourceTable from '@/my_project/ResourceListView/components/ResourceTable.vue';
    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    import type { Resource } from '@/my_project/types.ts';

    const resources = ref<Resource[]>([]);
    watchEffect(async () => {
        try {
            const response = await fetch(generateArchesURL('my_app:resources'));
            resources.value = await response.json();
        } catch (error) {
            console.error(error);
        }
    });
    </script>

    <template>
        <div class="resource-list-view">
            <ResourceTable :resources="resources" />
        </div>
    </template>

.. code-block:: vue

    <!-- Good: fetching as close as possible to where data is rendered -->

    <!-- ResourceListView.vue -->
    <script setup lang="ts">
    import ResourceTable from '@/my_project/ResourceListView/components/ResourceTable.vue';
    </script>

    <template>
        <div class="resource-list-view">
            <ResourceTable />
        </div>
    </template>


    <!-- ResourceTable.vue -->
    <script setup lang="ts">
    import { ref, watchEffect } from 'vue';

    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    import type { Resource } from '@/my_project/types.ts';

    const resources = ref<Resource[]>([]);
    watchEffect(async () => {
        try {
            const response = await fetch(generateArchesURL('my_app:resources'));
            resources.value = await response.json();
        } catch (error) {
            console.error(error);
        }
    });
    </script>

    <template>
        <table>
            <tbody>
                <tr
                    v-for="resource in resources"
                    :key="resource.id"
                >
                    <td>{{ resource.displayName }}</td>
                </tr>
            </tbody>
        </table>
    </template>
      
**Why?**

- **Encapsulation**: Data-fetch logic lives alongside the view that consumes it.
- **Limited prop drilling**: Minimizes passing data through unrelated parents.
- **Error isolation**: Failures are handled locally, without cascading side effects.

Primitives First
----------------

When a component only needs part of a model, pass only what it needs — not the whole object.

.. code-block:: vue

    <!-- Bad: passing a whole Resource model just to render a label -->
    <SubmitButton :resource="selectedResource" />

    <!-- Good: pass only what the component actually needs -->
    <SubmitButton :label="selectedResource.displayName" />

**Why?**

- **Explicit API**: Readers, tools, and developers see exactly which fields the component needs.
- **Immutable flow**: Primitives can't be mutated in place, preserving one-way data flow.
- **Efficient updates**: Changes to unused object properties won't force re-renders.

Derived State
-------------

If a component's sole responsibility is to derive or summarize data, pass the raw data and let it compute internally.

.. code-block:: vue

    <script setup lang="ts">
    import { ref, watchEffect } from 'vue';

    import OrderSummary from '@/my_project/OrderSummary.vue';

    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    import type { Order } from '@/my_project/types.ts';

    // Raw data fetched here
    const orders = ref<Order[]>([]);
    watchEffect(async () => {
        try {
            const response = await fetch(generateArchesURL('my_app:orders'));
            orders.value = await response.json();
        } catch (error) {
            console.error(error);
        }
    });
    </script>

    <template>
        <!-- OrderSummary receives the full list and does its own computing -->
        <OrderSummary :orders="orders" />
    </template>

When multiple children need the same computed value, derive once in the parent and pass primitives to avoid duplication and ensure consistency.

.. code-block:: vue

    <script setup lang="ts">
    import { ref, computed, watchEffect } from 'vue';

    import OrderSummary from '@/my_project/OrderSummary.vue';
    import OrderDetails from '@/my_project/OrderDetails.vue';

    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    import type { Order } from '@/my_project/types.ts';

    // Raw data fetched here
    const orders = ref<Order[]>([]);
    watchEffect(async () => {
        try {
            const response = await fetch(generateArchesURL('my_app:orders'));
            orders.value = await response.json();
        } catch (error) {
            console.error(error);
        }
    });

    // Derived state: compute once in the parent
    const totalOrders = computed(() => orders.value.length);
    </script>

    <template>
        <!-- Pass the computed value to both children -->
        <OrderSummary :total-orders="totalOrders" />
        <OrderDetails :total-orders="totalOrders" />
    </template>

**Why?**

- **Performance**: Avoids recomputing derived values in multiple components.
- **Predictable props**: Child components receive only the exact values they need.
- **Consistency**: Ensures every consumer uses the same computed values, preventing drift.

Event Emission
--------------

Emit semantic events (kebab-case) with typed payloads:

.. code-block:: vue

    <script setup lang="ts">
    const ROW_SELECTED_EVENT = 'row-selected' as const;

    interface RowSelectedEvent { rowId: number }

    const emit = defineEmits<{
        (event: typeof ROW_SELECTED_EVENT, payload: RowSelectedEvent): void
    }>();

    function onRowClick(id: number) {
        emit(ROW_SELECTED_EVENT, { rowId: id });
    }
    </script>

**Why?**

- **Explicit contracts**: Consumers know exactly what events to expect and how to handle them.
- **Type safety**: TypeScript ensures the payload matches the expected structure.

The <script> Tag
==================

This block defines a component's logic. Follow these rules for clarity, consistency, and maintainability.

Coding Standards
----------------

**Script Scope**

All component logic must be declared inside ``<script setup>``, and ``<script setup>`` should always have TypeScript as the defined language.

.. code-block:: vue

    <!-- Good: scoped to component, using typescript -->
    <script setup lang="ts">
    import { ref } from 'vue';

    const count = ref(0);
    function incrementCount() { count.value++; }
    </script>

    <!-- Bad: global scope pollution, no typescript -->
    <script>
        let count = 0;
        function incrementCount() { count++; }
    </script>

**Why?**

- **TypeScript support**: Enables full TypeScript support directly within each component.
- **Scope safety**: All variables and functions are scoped to the component, preventing accidental global pollution.

**Function Declarations**

Use named ``function`` declarations for component methods; **do not** use anonymous/arrow functions or function expressions. Anonymous/arrow functions are allowed for inline callbacks (e.g., ``setTimeout``, ``Promise.then``, ``filter``, ``onMounted``, ``computed``, etc.).

.. code-block:: js

    // Bad: arrow function for component method
    const incrementCount = () => { count.value++; };

    // Bad: function expression for component method
    const incrementCount = function() { count.value++; };

    // Good: named function declaration for component method
    function incrementCount() { count.value++; }

    // Good: arrow function used for inline callback
    setTimeout(() => { count.value++; }, 1000);

**Why?**

- **Hoisting**: Named functions are hoisted, allowing them to be called before their declaration in the code. This can help avoid issues with function order and improve readability.
- **Debugging**: Named functions provide better stack traces and error messages, making issues easier to diagnose.

**Constants & Literals**

Declare fixed values in ``SCREAMING_SNAKE_CASE``. Extract string literals and magic numbers as named constants when their meaning isn't self-evident from context, or when they appear in more than one place.

.. code-block:: js

    // Bad: magic number and string literal
    function calculateTotal(price) {
        return price * 0.0825;
    }

    function isOrderComplete(order) {
        return order.status === 'PENDING';
    }

    // Good: named constants
    const TAX_RATE = 0.0825;
    const ORDER_STATUS_PENDING = 'PENDING';

    function calculateTotal(price) {
        return price * TAX_RATE;
    }

    function isOrderComplete(order) {
        return order.status === ORDER_STATUS_PENDING;
    }

**Why?**

- **Readability**: Named constants make the code more self-explanatory and easier to understand and debug.
- **Maintainability**: Changing a single constant is easier than searching for all occurrences of a magic number or string literal.

**Naming Conventions**

Use descriptive identifiers; avoid single-letter names.

.. code-block:: js

    // Bad: single-letter naming
    function doubleValue(x) { return x * 2; }

    // Good: descriptive naming
    function doubleValue(value) { return value * 2; }

**Why?**

- **Clarity**: Descriptive names provide context and meaning, making the code easier to read and understand.
- **Maintainability**: Clear names help future developers (or yourself) quickly grasp the purpose of variables and functions.

**Modularity & Reuse**

Extract non-UI logic (data transformations, business rules) into composables or utility modules.

.. code-block:: js

    // Bad: non-UI logic in component
    function calculateDiscount(price, discount) {
        return price - (price * discount);
    }

    // Good: non-UI logic in utility module
    import { calculateDiscount } from '@/my_project/utils/discounts.ts';

**Why?**

- **Separation of concerns**: Keeps UI logic separate from business logic, making components easier to read and maintain.
- **Reusability**: Composables and utility modules can be reused across multiple components, reducing code duplication.

**Side-Effects & Async Handling**

Avoid performing side-effects (API calls, timers, storage access, data formatting, etc.) at module scope in ``<script setup>``. For **data fetching**, use ``watchEffect`` — it runs immediately and re-runs automatically when its reactive dependencies change. Reserve ``onMounted`` (and other lifecycle hooks) for operations that require the DOM to be ready (e.g. measuring elements, initializing a map library). Always wrap async operations in ``try/catch``, handle errors explicitly, and surface failures to the UI or calling code.

.. code-block:: vue

    <script setup lang="ts">
    import { ref, watchEffect, onMounted } from 'vue';
    import { generateArchesURL } from '@/arches/utils/generate-arches-url.ts';

    const data = ref(null);

    // Bad: module scope side-effect
    fetchData(); // runs immediately when the module loads, before the component is ready

    // Good: data fetching with watchEffect
    watchEffect(async () => {
        try {
            const response = await fetch(generateArchesURL('my_app:data'));
            data.value = await response.json();
        } catch (error) {
            console.error(error);
        }
    });

    // Good: DOM-dependent work in onMounted
    onMounted(() => {
        mapInstance.initialize(document.getElementById('map'));
    });
    </script>

**Why?**

- **Predictability**: Side-effects should only occur in controlled environments to avoid unexpected behavior.
- **Reactivity**: ``watchEffect`` automatically tracks reactive dependencies and re-fetches when they change, without needing ``immediate: true``.
- **Error handling**: Wrapping async operations in ``try/catch`` allows for graceful error handling and user feedback.

**Type Safety**

Import and use explicit types; avoid use of the ``any`` type. Annotate all function return types.

.. code-block:: typescript

    // Bad: using any type
    function fetchData(): any {
        return fetch(generateArchesURL('my_app:data')).then(response => response.json());
    }

    // Good: explicit type annotation
    interface User {
        id: number;
        name: string;
    }

    function fetchData(): Promise<User[]> {
        return fetch(generateArchesURL('my_app:data')).then(response => response.json());
    }

**Why?**

- **Type safety**: Using explicit types helps catch errors at compile time, reducing runtime issues.
- **Documentation**: Type annotations serve as documentation for function behavior and expected input/output.

Import Pathing
--------------

**Use project alias**

Use ``@/…`` for all local imports; avoid raw relative paths.

.. code-block:: js

    // Bad: raw relative path
    import { fetchData } from '../../utils/fetch-data.ts';

    // Good: project alias
    import { fetchData } from '@/project_name/utils/fetch-data.ts';

**Why?**

- **Readability**: Project aliases make it clear where the module is located without needing to trace relative paths.
- **Maintainability**: Avoids issues with deep nesting and makes it easier to refactor or reorganize the project structure.

Import Order
------------

Import lines must be grouped and ordered as follows:

1. **Vue core**
2. **Third-party modules**
3. **Vue components** (third-party → arches core → arches applications → local)
4. **Utilities/composables** (third-party → arches core → arches applications → local)
5. **Types** (third-party → arches core → arches applications → local)

.. code-block:: vue

    <script setup lang="ts">
    // 1. Vue core
    import { ref, computed } from 'vue';

    // 2. Third-party modules
    import { useGettext } from 'vue3-gettext';

    // 3. Vue components
    import { ProgressSpinner } from 'primevue/progressspinner';
    import ArchesCoreComponent from '@/arches/components/ArchesCoreComponent.vue';
    import ArchesAppComponent from '@/arches_app/components/ArchesAppComponent.vue';
    import MyComponent from '@/project_name/components/MyComponent.vue';

    // 4. Utilities/composables
    import { doSomeArchesCoreLogic } from '@/arches/utils/do-some-arches-core-logic.ts';
    import { doSomeArchesAppLogic } from '@/arches_app/utils/do-some-arches-app-logic.ts';
    import { fetchData } from '@/project_name/utils/fetch-data.ts';

    // 5. Types
    import type { Component } from 'vue';
    import type { ArchesCoreType } from '@/arches/types.ts';
    import type { ArchesAppType } from '@/arches_app/types.ts';
    import type { UserProfile } from '@/project_name/types.ts';

    // Your component logic here
    </script>

Declaration Order
-----------------

Within your ``<script setup>`` block, organize declarations in this sequence:

0. **Static constants**
1. **`defineProps`**
2. **`defineEmits`/`defineExpose`**
3. **Dependency injection**
4. **Set up composables/utilities**
5. **Component state**
6. **Computed properties**
7. **Watchers**
8. **Lifecycle hooks**
9. **Methods/functions**

.. code-block:: vue

    <script setup lang="ts">
    import { ref, computed, watch, watchEffect, onMounted, inject } from 'vue';
    import { useGettext } from 'vue3-gettext';

    import type { Item } from '@/project_name/types.ts';

    // 0. Static constants
    const POLL_MS = 5000;

    // 1. defineProps
    const props = defineProps<{ id: number }>();

    // 2. defineEmits/defineExpose
    const emit = defineEmits<{ (event: 'loaded'): void }>();
    defineExpose({ myMethod: myMethod });

    // 3. Dependency injection
    const api = inject('apiClient')!;

    // 4. Set up composables/utilities
    const { $gettext } = useGettext();

    // 5. Component state
    const data = ref<Item[]>([]);
    const isLoading = ref(true);

    // 6. Computed properties
    const hasData = computed(() => data.value.length > 0);

    // 7. Watchers
    watchEffect(async () => {
        await loadData();
    });

    watch(() => props.id, async (newId) => {
        await loadData();
    }, { immediate: true });

    // 8. Lifecycle hooks
    onMounted(() => {
        // reserved for DOM-dependent work
    });

    // 9. Methods/functions
    async function loadData() {
        try {
            isLoading.value = true;
            data.value = await api.fetchItems(props.id);
        } catch (error) {
            console.error(error);
        } finally {
            isLoading.value = false;
            emit('loaded');
        }
    }
    </script>

The <template> Tag
====================

Defines the component's UI. Keep templates clear, consistent, and easy to scan.

Attribute Ordering & Formatting
-------------------------------

When declaring attributes in your ``<template>``, group and order them as follows:

1. **Directives** (e.g. ``v-for``, ``v-if``)
2. **Slots** (e.g. ``v-slot:header="…"``)
3. **Static attributes** (e.g. ``id``, ``class``)
4. **Dynamic props** (e.g. ``:prop="…"``)
5. **Event listeners** (e.g. ``@click="…"``, ``@click.prevent="…"``)

**Inline vs. multiline** — One attribute: keep on the same line as the tag. Two or more: one per line, indented under the tag.

**Explicit assignment** — Always write ``prop="value"`` or ``:prop="value"``. Do not use shorthand (``:prop`` without a value).

**Kebab-case** — All attribute names, including custom props and events, must use kebab-case.

.. code-block:: vue
    
    <template>
        <!-- Good: grouped, ordered, multiline, kebab-case -->
        <UserCard
            v-if="isVisible"
            v-slot:default="{ user }"
            id="user-card"
            class="card highlight"
            :avatar-url="user.avatarUrl"
            :is-active="user.isActive"
            @mouseover="onHover"
            @submit.prevent="onSubmit"
        />

        <!-- Bad: unordered, inline, camelCase -->
        <UserCard id="userCard" :avatarUrl="user.avatarUrl" @submit.prevent="onSubmit" v-if="isVisible"/>
    </template>

**Why?**

- **Readability**: Consistent ordering and formatting make it easier to scan and understand the template.
- **Maintainability**: Clear structure helps future developers (or yourself) quickly grasp the component's purpose and behavior.

Self-Closing Tags
-----------------

Use self-closing syntax for elements or components without children:

.. code-block:: vue

    <template>
        <LogoIcon />
        <img src="@/assets/logo.png" alt="Logo" />
    </template>

**Why?**

- **Clarity**: Self-closing tags clearly indicate that the element has no children, improving readability.
- **Consistency**: Using self-closing syntax for void elements (e.g., `<img>`, `<input>`) maintains a consistent style throughout the codebase.

Logic in Templates
------------------

Simple ternaries are acceptable. Compound or nested ternaries, chained method calls, and heavy expressions must be moved into ``computed`` properties or methods.

.. code-block:: vue

    <!-- Good: simple ternary -->
    <div :class="isActive ? 'active' : 'inactive'" />

    <!-- Bad: compound ternary — move to computed -->
    <div>{{ isLoading ? '...' : hasError ? errorMessage : displayText }}</div>

    <!-- Bad: chained method call — move to computed or method -->
    <div>{{ items.filter(isActive).map(formatLabel).join(', ') }}</div>

**Why?**

- **Readability**: Templates should be easy to read and understand at a glance.
- **Performance**: Heavy computations in templates can lead to unnecessary re-renders and performance issues.

Text in Templates
-----------------

**Internationalization** — Wrap all user-facing strings with ``$gettext()``. For runtime values, use ``%{placeholder}`` syntax and pass a values object as the second argument. Never concatenate translated strings.

**When to use interpolate()** — ``$gettext(msg, values)`` handles interpolation for most cases. Use ``interpolate()`` explicitly in two situations:

- The translation contains **HTML markup** that will be rendered via ``v-html``. Omit the third argument so substituted values are HTML-escaped, preventing markup injection.
- A substituted value may contain **literal angle brackets** (e.g. ``Aircraft <by type>``). Pass ``true`` as the third argument to prevent those characters from being HTML-escaped.

**No loose text nodes** — Surround plain text with an inline element (e.g. ``<span>``) or semantic tag.

.. code-block:: vue

    <script setup lang="ts">
    import { useGettext } from 'vue3-gettext';

    import type { RelationshipGroup } from '@/project_name/types.ts';

    const { $gettext, interpolate } = useGettext();

    const { group, authorName } = defineProps<{
        group: RelationshipGroup;
        authorName: string;
    }>();

    // group.label may contain literal angle brackets (e.g. "Aircraft <by type>")
    // — pass true so they are not HTML-escaped in the returned string
    function getGroupLabel(): string {
        return interpolate(
            $gettext('Top Concept Of: %{parent}'),
            { parent: group.label },
            true,
        );
    }
    </script>

    <template>
        <div class="concept-detail">
            <!-- Bad: concatenation breaks translator context -->
            {{ $gettext('Group:') }} {{ group.label }}

            <!-- Good: standard interpolation — values passed directly to $gettext -->
            <h2>{{ $gettext('Group: %{label}', { label: group.label }) }}</h2>

            <!-- Good: interpolate() with true for values that may contain angle brackets -->
            <span>{{ getGroupLabel() }}</span>

            <!-- Good: interpolate() for HTML in translations rendered via v-html -->
            <!-- no true — values are HTML-escaped to prevent markup injection -->
            <span v-html="interpolate($gettext('Added by <b>%{name}</b>'), { name: authorName })" />
        </div>
    </template>

**Why?**

- **Translator context**: Placeholders keep the full sentence intact in ``.po`` files, giving translators the context they need to produce accurate translations.
- **HTML safety**: ``interpolate()`` HTML-escapes substituted values by default, preventing markup injection via ``v-html``. Pass ``true`` only when substituted values are plain text that may legitimately contain angle brackets.
- **Semantic HTML**: Using inline elements or semantic tags improves accessibility and SEO by providing context to screen readers and search engines.

The <style> Tag
=================

Defines component-scoped CSS. Follow these rules for responsive, maintainable, and themeable styles.

Scope
-----

Prefer ``<style scoped>`` to ensure styles are applied only to the component. Reserve global styles and design tokens for your global CSS or theme files unless absolutely necessary.

.. code-block:: vue

    <!-- Bad: global styles -->
    <style>
        .header {
            color: var(--p-primary-500);
        }
    </style>

    <!-- Good: scoped styles -->
    <style scoped>
        .header {
            color: var(--p-primary-500);
        }
    </style>

**Why?**

- **Isolation**: Scoped styles prevent unintended side effects on other components, ensuring consistent styling.
- **Maintainability**: Changes to a component's styles won't affect other components, reducing the risk of introducing undesired behavior.

Layout Patterns
---------------

**Flexbox & Grid only** — Use ``display: flex`` for one-dimensional layouts and ``display: grid`` for two-dimensional arrangements.

**Use gap** — Space items with ``gap``; do not rely on margins for core layout.

**No legacy hacks** — Never use ``float`` or other outdated layout techniques.

**Single-line vs. multi-line selectors** — Use single-line selectors for a single atomic override; use multi-line selectors when grouping multiple rules.

.. code-block:: css

    /* Bad: single-line selector for multiple rules */
    .item { display: flex; gap: 1rem; }

    /* Good: single-line selector for one rule */
    .item { display: flex; }

    /* Good: multi-line selector for multiple rules */
    .item {
        display: flex;
        gap: 1rem;
    }

**Why?**

- **Flexibility**: Flexbox and Grid provide powerful layout capabilities for modern web applications.
- **Maintainability**: Using `gap` simplifies spacing management and reduces the need for complex margin calculations.
- **Scanability**: Single-line selectors signal a single atomic override and are easy to scan past. Multi-line formatting means each property appears on its own line in diffs, making code review clearer.

Units & Sizing
--------------

**rem for nearly everything** — Use ``rem`` units for spacing, typography, gaps, borders, and other dimensional values.

**Viewport units sparingly** — Reserve ``vh``/``vw`` for elements that must span the viewport (e.g. full-screen sections or modals).

**Percentages for fluid layouts** — Apply ``%`` when you need relative sizing (e.g. fluid widths in responsive grids).

**No px** — Avoid ``px`` units entirely to ensure scalability, accessibility, and consistent theming.

.. code-block:: css

    /* Bad: using px units */
    .container { width: 800px; padding: 20px; }

    /* Good: using rem units */
    .container { width: 50rem; padding: 1.25rem; }

    /* Good: using percentage for fluid layout */
    .container { width: 100%; }

**Why?**

- **Scalability**: Using `rem` and `%` units allows for better scaling across different screen sizes and resolutions.
- **Accessibility**: Relative units ensure that text and elements can be resized according to user preferences, improving accessibility.

Offsets & Positioning
---------------------
**No single-side offsets** — Use logical properties (``margin-inline-start``, ``margin-block-start``) instead of physical directional properties like ``margin-left`` or ``margin-top``.

**No negative margins** — Negative ``margin-*`` values are forbidden.

.. code-block:: css

    /* Bad: negative margin, not using logical properties */
    .container .item { margin-left: -1rem; }

    /* Good: no negative margin, using logical properties */
    .container { padding-inline-start: 1rem; }
    .item { margin-inline-start: 0; }

**Why?**

- **Logical properties**: Using logical properties ensures consistent behavior across different language displays (e.g. left-to-right vs. right-to-left).
- **Avoiding layout shifts**: Negative margins can lead to unexpected layout shifts and make it harder to maintain a consistent design.

No `calc()`
-----------

Avoid ``calc()`` for layout problems that flexbox or grid can solve directly.

.. code-block:: css

    /* Bad: using calc() to fake a two-column layout */
    .sidebar { width: calc(100% - 800px); }
    .content { width: 800px; }

    /* Good: use grid instead */
    .container {
        display: grid;
        grid-template-columns: 1fr auto;
    }

**Why?**

- Layout math in `calc()` is often a sign that flexbox or grid would be a cleaner solution.
- Mixing `calc()` with hardcoded pixel values creates fragile layouts that break when surrounding elements change.

Theming & Colors
----------------

**Design tokens only** — Always reference design tokens instead of raw values.

**Centralize & document** — Keep all tokens (colors, typography scales, breakpoints) in a single theme file.

**Semantic layers** — Build on top of raw palette entries with semantic tokens (e.g. ``--color-success``) so UI intent drives your choices.

**Light/dark support** — Define variants for both modes in your theme preset.

.. code-block:: js

    import { definePreset } from '@primeuix/themes';
    import { ArchesPreset } from "@/arches/themes/default.ts";

    export const MyTheme = definePreset(ArchesPreset, {
        semantic: {
            colorScheme: {
                light: {
                    primary: { color: '{primary.500}', contrast: '{primary.50}' },
                    success: { color: 'green', contrast: '{surface.900}' }
                },
                dark: {
                    primary: { color: '{primary.300}', contrast: '{surface.900}' }
                }
            }
        }
    });

**Consuming tokens in CSS** — PrimeVue tokens are available as CSS custom properties using the ``--p-`` prefix (set by Arches's ``DEFAULT_THEME``). Reference them directly in ``<style scoped>`` blocks.

.. code-block:: css

    /* Semantic color tokens */
    .my-heading { color: var(--p-primary-500); }
    .my-card { background: var(--p-surface-0); border: 0.0625rem solid var(--p-surface-200); }

    /* Never use raw values */
    .my-heading { color: #579ddb; }  /* Bad */

**Why?**

- **Consistency**: Using design tokens ensures a consistent look and feel across the application.
- **Maintainability**: Centralizing tokens makes it easier to update and manage styles.
- **Dark mode**: Token values automatically swap between light and dark variants — raw values do not.

Selector Naming
---------------

Prefix selectors with the component's root class, then chain child class names:

.. code-block:: css

    .user-card {
        display: flex;
        flex-direction: column;
        gap: 1rem;
    }
    .user-card .header {
        display: grid;
        grid-template-columns: 1fr auto;
        gap: 0.5rem;
    }
    .user-card .header .title {
        font-size: 1.5rem;
        color: var(--p-primary-500);
    }

**Why?**

- **Clarity**: Dot-delineated selectors make the component's internal structure self-documenting — a reader can understand the component's layout from the CSS alone.
- **Specificity control**: Chaining from the root class makes specificity intentional and predictable, avoiding unexpected override order within the component.

Testing
=======

To ensure the reliability and functionality of our Vue components, we use **Vitest** together with **Vue Test Utils**. Vitest is a fast, modern test runner that integrates seamlessly with Vite, while Vue Test Utils provides utilities to mount components and inspect their rendered output.

Test Location & Naming
----------------------

- Co-locate tests next to components, in the same directory.  
- Test files must end with a ``.spec.ts`` suffix.  

.. code-block:: shell

    src/
    └── my_project/
        ├── CustomApplication.vue
        ├── CustomApplication.spec.ts
        ├── utils.ts
        ├── utils.spec.ts
        ├── widgets/
        │   └── CustomWidget/
        │       ├── CustomWidget.vue
        │       └── CustomWidget.spec.ts
        └── reports/
            └── CustomReport/
                ├── CustomReport.vue
                └── CustomReport.spec.ts

**Why?**

- **Organization**: Grouping tests by component or utility helps maintain a clean project structure.
- **Ease of navigation**: Developers can quickly locate tests related to a specific component or utility without searching through a separate test directory.

Writing Frontend Tests
----------------------

When crafting your tests, adhere to these best practices:

**Isolation** — Test components with real children where possible. Only stub external services, API calls, and third-party libraries that are difficult to mount in jsdom.

**Coverage** — Cover all code paths, including edge cases (error states, conditional rendering, emitted events).

**Readability** — Use clear, descriptive test names and group related tests with ``describe`` blocks.

**Async handling** — Use ``flushPromises`` or ``await nextTick()`` after triggering asynchronous updates.

**Cleanup** — Unmount or destroy wrappers if they persist between tests (though Vitest's JSDOM resets per test by default).

.. code-block:: vue

    <!-- src/components/CounterButton.vue -->
    <script setup lang="ts">
    import { ref } from 'vue';

    const count = ref(0);
    function increment() {
        count.value++;
    }
    </script>

    <template>
        <button @click="increment" class="counter">
            {{ count }}
        </button>
    </template>

    <style scoped>
    .counter { padding: 0.5rem 1rem; }
    </style>

.. code-block:: js

    // src/components/CounterButton.spec.ts
    import { describe, it, expect } from 'vitest';
    import { mount, flushPromises } from '@vue/test-utils';
    import CounterButton from '@/my_project/components/CounterButton.vue';

    describe('CounterButton.vue', () => {
        it('mounts and displays initial count', () => {
            const wrapper = mount(CounterButton);
            expect(wrapper.text()).toContain('0');
        });

        it('increments count on click', async () => {
            const wrapper = mount(CounterButton);
            const button = wrapper.find('button');
            await button.trigger('click');
            await flushPromises();
            expect(wrapper.text()).toContain('1');
        });
    });

**Why?**

- **Isolation**: Testing components in isolation helps identify issues more easily and ensures that tests are not affected by other components.
- **Readability**: Clear and descriptive test names make it easier for developers to understand the purpose of each test.
- **Maintainability**: Well-structured tests are easier to maintain and update as the codebase evolves.

Running Frontend Tests
----------------------

Use the following npm scripts in your terminal:

.. code-block:: shell

    # Run all tests once
    npm run vitest

    # Run a specific test file
    npm run vitest -- src/components/CounterButton.spec.ts

    # Watch mode — re-runs on file changes
    npm run vitest -- --watch

    # Run with coverage report (output appears under coverage/)
    npm run vitest -- --coverage
