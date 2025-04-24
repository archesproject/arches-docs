######################
Arches Vue Style Guide
######################

Purpose
=======

The purpose of this style guide is to establish a unified coding style and set of conventions that all contributors should adhere to when writing code for Arches. By following these guidelines, we aim to:

- Improve code readability and maintainability
- Facilitate collaboration among developers
- Enhance the overall quality and consistency of Arches software, Arches projects, and Arches applications

Basis for Style Guide
=====================

This style guide for Arches is built on top of the standard Vue.js and TypeScript style guides. As such, it inherits and extends the conventions and best practices outlined in those guides. 

Any coding style, formatting, or conventions not explicitly covered in this document should be referenced from the official Vue.js and TypeScript style guides. It's important to maintain consistency with these standard guidelines to ensure compatibility and familiarity for developers working with Vue.js and TypeScript projects.

For Vue.js, you can refer to the `official Vue style guide <https://vuejs.org/style-guide/>`_. 

Similarly, for TypeScript, you can refer to the `official TypeScript style guide <https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html>`_.

Contributions
=============

This style guide is a living document that evolves over time. We welcome contributions from the community to improve and expand this guide further. If you have suggestions, feedback, or would like to contribute to the style guide, please reach out to us via the `Arches Forum <https://community.archesproject.org/>`_.

Project Structure
=================

Naming Conventions
~~~~~~~~~~~~~~~~~~

- **Arches entity directories**:
  Use plural, lowercase names to reflect domain concepts.  
  e.g. ``cards/``, ``widgets/``, ``reports/``

- **Vue component directories**:  
  One folder per component, named in PascalCase.  
  e.g. ``CustomComponent/``

- **Non-Vue component directories**:  
  Utility or helper folders in kebab-case.  
  e.g. ``custom-utility/``, ``date-utils/``

- **Vue components**:  
  File names in PascalCase with a ``.vue`` extension.  
  e.g. ``UserCard.vue``, ``MapViewer.vue``

- **Utilities & helpers**:  
  Use kebab-case, file extension ``.js`` or ``.ts``.  
  e.g. ``fetch-api.ts``, ``format-date.js``

- **Type files**:  
  Single-purpose type definitions in kebab-case, ``.ts``.  
  e.g. ``user-profile.ts``, ``map-types.ts``

Top-Level Structure
~~~~~~~~~~~~~~~~~~~

Top-level directories **must** align with Arches concepts (e.g., cards, widgets, reports) when such delineation is required. Otherwise, consolidate everything under a single app-level directory.


.. code-block:: shell

    src/
    └── project_name/
        ├── plugins
        ├── reports/
        │   └── CustomReport/
        │       ├── components
        │       └── CustomReport.vue
        ├── widgets
        └── types
        └── utils.ts

.. code-block:: shell

    src/
    └── project_name/
        ├── components/
        │   └── CustomComponent.vue
        ├── CustomApplication.vue
        ├── types
        └── utils.ts


Component Folder Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~

At every level:

- **Component files with sub-components** **must** reside in a folder named after the component.
- **Dependent components** **must** live in a `components/` subdirectory within their **parent component's** folder.
- **Shared components** (used by more than one parent) **must** be elevated to the `components/` directory at the level of the **highest parent component** that uses them.

.. code-block:: shell

    src/project_name/
    ├── CustomApplication.vue
    └── components/
        └── CustomDashboard/
            ├── CustomDashboard.vue
            └── components/
                └── DashboardTable/
                    └── DashboardTable.vue/
                        └── components/
                            ├── CustomHeader.vue
                            ├── TableSection.vue
                            └── UpdatedFooter.vue


Component Structure
===================

Single-File Components
~~~~~~~~~~~~~~~~~~~~~~

Single-File Components (SFCs) are the preferred way to define Vue components. They encapsulate the template, script, and style in a single file, making it easier to manage and understand the component's structure.

.. code-block:: js

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

Component Decomposition
~~~~~~~~~~~~~~~~~~~~~~~

Components should be decomposed into smaller, reusable components whenever possible. This promotes reusability and maintainability. Aim for a single responsibility per component.

.. code-block:: shell

    widgets/
    └── CustomWidget/
        ├── components/
        │   ├── CustomWidgetEditor.vue
        │   └── CustomWidgetViewer.vue
        └── CustomWidget.vue

Passing Data
~~~~~~~~~~~~

- **Fetch Proximity**:  
  Fetch data in the component that actually renders it. Don't lift network calls higher than needed.

.. code-block:: js

    <!-- Bad: fetching at a high-level parent when only the table needs it -->

    <!-- Dashboard.vue -->
    <script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import UserTable from '@/my_project/Dashboard/components/UserTable.vue'

    // Parent fetches users even if only UserTable displays them
    const users = ref([])
    onMounted(async () => {
        users.value = await fetch('/api/users').then(resp => resp.json())
    })
    </script>

    <template>
        <div class="dashboard">
            <h1>Dashboard</h1>
            <!-- Data passed down via prop -->
            <UserTable :users="users" />
        </div>
    </template>


    <!-- Good: fetching as close as possible to where data is rendered -->

    <!-- Dashboard.vue -->
    <script setup lang="ts">
    // Parent no longer fetches users
    </script>

    <template>
        <div class="dashboard">
            <h1>Dashboard</h1>
            <!-- Child responsible for its own data -->
            <UserTable />
        </div>
    </template>


    <!-- UserTable.vue -->
    <script setup lang="ts">
    import { ref, onMounted } from 'vue'
    import type { User } from '@/types'

    // Fetch proximity: fetch here since this component renders the list
    const users = ref<User[]>([])
    onMounted(async () => {
        users.value = await fetch('/api/users').then(resp => resp.json())
    })
    </script>

    <template>
        <table>
            <tbody>
                <tr v-for="user in users" :key="user.id">
                    <td>{{ user.name }}</td>
                    <td>{{ user.email }}</td>
                </tr>
            </tbody>
        </table>
    </template>

- **Primitives First**:  
  Pass simple values (strings, numbers, booleans, small arrays/objects) instead of entire model objects whenever possible.

.. code-block:: html

    <!-- Bad: passing entire model objects -->
    <UserProfile :user="currentUser" />

    <!-- Good: passing only primitive values -->
    <UserProfile
        :user-id="currentUser.id"
        :user-name="currentUser.name"
        :is-admin="currentUser.isAdmin"
    />

- **Derived State**:  
  Compute any summaries or transformations in the consumer component and pass those primitives down.

.. code-block:: js

    <!-- ParentComponent.vue -->
    <script setup lang="ts">
    import { ref, computed, onMounted } from 'vue'
    import type { Order } from '@/types'

    // Raw data fetched here
    const orders = ref<Order[]>([])
    onMounted(async () => {
        orders.value = await fetch('/api/orders').then(r => r.json())
    })

    // Derived state: compute primitives
    const orderCount = computed(() => orders.value.length)
    const totalSales = computed(() =>
        orders.value.reduce((sum, order) => sum + order.amount, 0)
    )
    </script>

    <template>
        <!-- Pass only the computed primitives -->
        <OrderSummary
            :count="orderCount"
            :total-sales="totalSales"
        />
    </template>

    <!-- OrderSummary.vue -->
    <script setup lang="ts">
    const props = defineProps<{
        count: number
        totalSales: number
    }>()
    </script>

    <template>
        <div class="order-summary">
            <p>Total Orders: {{ props.count }}</p>
            <p>Total Sales: {{ props.totalSales }}</p>
        </div>
    </template>

- **Event Emission**:  
  Emit semantic events (kebab-case) with typed payloads:

.. code-block:: js

    <script setup lang="ts">
    interface RowSelectedEvent { rowId: number }

    defineEmits<{
        (e: 'row-selected', payload: RowSelectedEvent): void
    }>()

    function onRowClick(id: number) {
        emit('row-selected', { rowId: id })
    }
    </script>

- **Slots**:  
  Use scoped slots for maximum flexibility; name them clearly

.. code-block:: html

    <MyTable>
        <template #header>
            {{ $gettext('Table Header') }}
        </template>
        <template #row="{ row }">
            <MyRow :data="row" />
        </template>
    </MyTable>


The `<script>` Tag
==================

This block defines a component's logic. Follow these rules for clarity, consistency, and maintainability.

Coding Standards
~~~~~~~~~~~~~~~~

- **Script Scope**:  
  All component logic **must** reside within `<script setup>`—no module-scope side-effects.

- **Function Declarations**:  
    - Use named `function` declarations for component methods; **do not** use anonymous functions or function expressions.
    - Use of anonymous functions is allowed within parent functions (eg `setTimeout`, `Promise.then`, `filter`, `onMounted`, `computed`, etc.).

- **Constants & Literals**:  
    - Declare fixed values in `SCREAMING_SNAKE_CASE`.  
    - Declare all string literals and magic numbers as named constants.
      eg `const POLL_MS = 5000;` 

- **Naming Conventions**:  
  Use descriptive identifiers; avoid single-letter names.

- **Modularity & Reuse**:  
  Extract non-UI logic (data transformations, business rules) into composables or utility modules.  

- **Side-Effects & Async Handling**:  
    - No side-effects in the `<script>` tag. Encapsulate API calls, formatting logic, and other side-effects in lifecycle hooks or composables.
    - Wrap all async operations in `try/catch`, and surface or display errors appropriately.

- **Type Safety**:  
  Import and use explicit types; avoid `any`. Annotate all function return types.

Import Pathing
~~~~~~~~~~~~~~

**Use project alias** (`@/…`) for all local imports; avoid raw relative paths. e.g. 

.. code-block:: js

    // Bad: raw relative path
    import { fetchData } from '../../utils/fetch-data.ts'
    
    // Good: project alias
    import { fetchData } from '@/project_name/utils/fetch-data.ts' 

Import Order
~~~~~~~~~~~~~

Import lines should be grouped and ordered as follows:

1. **Vue core**  
2. **Third-party modules**  
3. **Third-party Vue components**  
4. **Local Vue components**  
5. **Local utilities/composables**  
6. **Third-party types**  
7. **Local types**  

.. code-block:: js

    <script setup lang="ts">
    // 1. Vue core
    import { ref, computed } from 'vue'

    // 2. Third-party modules
    import { useGettext } from 'vue3-gettext'

    // 3. Third-party Vue components
    import { ProgressSpinner } from 'primevue/progressspinner'

    // 4. Local Vue components
    import MyComponent from '@/project_name/components/MyComponent.vue'

    // 5. Local utilities/composables
    import { fetchData } from '@/project_name/utils/fetchData.ts'

    // 6. Third-party types
    import type { Component } from 'vue'

    // 7. Local types
    import type { UserProfile } from '@/project_name/types.ts'

    // Your component logic here
    </script>

Declaration Order
~~~~~~~~~~~~~~~~~

Within your `<script setup>` block, organize declarations in this sequence. Omit any steps that don’t apply.

1. **`defineProps`**  
2. **`defineEmits` / `defineExpose`**  
3. **Composables instantiation**:  
   e.g. `const { $gettext } = useGettext()`  
4. **Dependency injection**:  
   e.g. `const api = inject('apiClient')!`  
5. **Constants & configuration**:  
   - SCREAMING_SNAKE_CASE for truly constant values  
6. **Reactive state**:  
   - `const foo = ref(...)`  
7. **Computed properties**  
8. **Watches**  
9. **Lifecycle hooks**:  
   e.g. `onMounted()`, `onBeforeUnmount()`  
10. **Methods / functions**  

.. code-block:: js

    <script setup lang="ts">
    import { ref, computed, watch, onMounted, inject } from 'vue';
    import { useGettext } from 'vue3-gettext';
    import type { Item } from '@/project_name/types';

    // 1. defineProps
    const props = defineProps<{ id: number }>();

    // 2. defineEmits
    const emit = defineEmits<{ (e: 'loaded'): void }>();

    // 3. Composables instantiation
    const { $gettext } = useGettext();

    // 4. Dependency injection
    const api = inject('apiClient')!;

    // 5. Constants & configuration
    const POLL_MS = 5000;

    // 6. Reactive state
    const data = ref<Item[]>([]);
    const isLoading = ref(true);

    // 7. Computed properties
    const hasData = computed(() => data.value.length > 0);

    // 8. Watches
    watch(() => props.id, loadData, { immediate: true });

    // 9. Lifecycle hooks
    onMounted(() => {
      loadData();
    });

    // 10. Methods / functions
    async function loadData() {
      try {
        isLoading.value = true;
        data.value = await api.fetchItems(props.id);
      } catch (err) {
        console.error(err);
      } finally {
        isLoading.value = false;
        emit('loaded');
      }
    }
    </script>


The `<template>` Tag
====================

Defines the component's UI. Keep templates clear, consistent, and easy to scan.

Attribute Ordering & Formatting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When declaring attributes in your `<template>`, group and order them as follows. Within each group, sort attributes alphabetically.

1. **Directives** (e.g. `v-for`, `v-if`)  
2. **Slots** (e.g. `v-slot:header="…"` )
3. **Static attributes** (e.g. `id`, `class`)  
4. **Dynamic props** (e.g. `:prop="…"` )  
5. **Event listeners** (e.g. `@click="…"` )  
6. **Modifiers** (e.g. `@click.prevent="…"` )  

Formatting rules:

- **Inline vs. Multiline**  
    - **One attribute** → keep on the same line as the tag.  
    - **Multiple attributes** → one per line, indented under the tag.  
- **Explicit assignment**  
    - Always write `prop="value"` or `:prop="value"`.  
    - Do **not** use shorthand (`:prop` without value) or omit values.  
- **Kebab-case**  
    - All attribute names (including custom props and events) **must** use kebab-case.

.. code-block:: html

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

Self-Closing Tags
~~~~~~~~~~~~~~~~~

Use self-closing syntax for elements or components without children:

.. code-block:: html

    <template>
        <LogoIcon />
        <img src="@/assets/logo.png" alt="Logo" />
    </template>

Logic in Templates
~~~~~~~~~~~~~~~~~~

- **No complex logic**  
    - Avoid ternaries, chained method calls, or heavy expressions.  
    - Move conditions and transformations into `computed` or methods.  

.. code-block:: html

    <!-- Good: simple v-if, logic lives in computed -->
    <template>
        <div v-if="isVisible">{{ displayText }}</div>
    </template>

    <!-- Bad: inline ternary and method call -->
    <template>
        <div>{{ isVisible ? formatText(user.name) : '—' }}</div>
    </template>

Text in Templates
~~~~~~~~~~~~~~~~~

- **Internationalization**  
  - Wrap all user-facing strings with `$gettext()`.  
  - Avoid string concatenation; use formatting placeholders.

- **No loose text nodes**  
  - Surround plain text with an inline element (e.g., `<span>`) or semantic tag.  

.. code-block:: html

    <!-- Good -->
    <template>
        <div>
            <span>{{ $gettext('Hello, world!') }}</span>
            
            <Button @click="handleClick">
                {{ $gettext('Click me!') }}
            </Button>
        </div>
    </template>

    <!-- Bad: unwrapped text node -->
    <template>
        <div>
            {{ $gettext('Hello, world!') }}

            <Button @click="handleClick">
                {{ $gettext('Click me!') }}
            </Button>
        </div>
    </template>

The `<style>` Tag
=================

Defines component-scoped CSS. Follow these rules for responsive, maintainable, and themeable styles.

Scope
~~~~~

- **Scoped styles**  
    - Prefer to use `<style scoped>` to ensure styles are applied only to the component.  
    - Reserve global styles and design tokens for your global CSS or theme files unless absolutely necessary.

Layout Patterns
~~~~~~~~~~~~~~~

- **Flexbox & Grid only**  
    Use `display: flex` for one-dimensional layouts and `display: grid` for two-dimensional arrangements.  
- **Use `gap`**  
    Space items with `gap`; do **not** rely on margins for core layout.  
- **No legacy hacks**  
    Never use `float`, `inline-block`, or other outdated techniques.

Units & Sizing
~~~~~~~~~~~~~~

- **`rem` for nearly everything**  
    Use `rem` units for spacing, typography, gaps, borders, and other dimensional values.

- **Viewport units sparingly**  
    Reserve `vh`/`vw` for elements that must span the viewport (e.g., full-screen sections or modals).

- **Percentages for fluid layouts**  
    Apply `%` when you need relative sizing (e.g., fluid widths in responsive grids).

- **No `px`**  
    Avoid `px` units entirely to ensure scalability, accessibility, and consistent theming.

Offsets & Positioning
~~~~~~~~~~~~~~~~~~~~~
- **No hard-coding single-side offsets**  
    Instead of using `margin-left`, `margin-top`, etc., use logical properties like `margin-inline-start` and `margin-block-start`. This ensures proper alignment in different writing modes.

.. code-block:: css

    /* Bad */
    .Overlay {
        margin-right: 2rem;
    }

    /* Good */
    <style scoped>
        .Overlay {
            margin-inline-end: 2rem;
        }
    </style>

- **No negative margins**  
    Negative `margin-*` values are forbidden.

No `calc()`
~~~~~~~~~~~

- The `calc()` function is forbidden in component styles.

Theming & Colors
~~~~~~~~~~~~~~~~

- **No hard-coded colors**  
    Prefer to reference design tokens, e.g. `var(--theme-primary)`.  
- **Centralize tokens**  
    Define colors, typography, spacing scales, and breakpoints in your theme files.

Selector Naming
~~~~~~~~~~~~~~~

- **Dot-delineated hierarchy**  
    Prefix selectors with the component's root class, then chain child class names:

.. code-block:: css

    <style scoped>
        .user-card {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .user-card.header {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 0.5rem;
        }
        .user-card.header.title {
            font-size: 1.5rem;
            color: var(--theme-primary);
        }
    </style>


Testing
=======

To ensure the reliability and functionality of our Vue components, we use **Vitest** together with **Vue Test Utils**. Vitest is a fast, modern test runner that integrates seamlessly with Vite, while Vue Test Utils provides utilities to mount components and inspect their rendered output.

Test Location & Naming
~~~~~~~~~~~~~~~~~~~~~~

- Co-locate tests next to components, in the same directory.  
- Test files must end with a ``.spec.ts`` suffix.  
- Example structure:

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

Writing Tests
~~~~~~~~~~~~~

When crafting your tests, adhere to these best practices:

- **Isolation**  
  Mount each component on its own—stub or mock child components to pinpoint issues precisely.

- **Coverage**  
  Cover all code paths, including edge cases (error states, conditional rendering, emitted events).

- **Readability**  
  Use clear, descriptive test names and group related tests with ``describe`` blocks.

- **Async Handling**  
  Use ``flushPromises`` or ``await nextTick()`` after triggering asynchronous updates.

- **Cleanup**  
  Unmount or destroy wrappers if they persist between tests (though Vitest's JSDOM resets per test by default).

.. code-block:: js

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
            Count: {{ count }}
        </button>
    </template>

    <style scoped>
    .counter { padding: 0.5rem 1rem; }
    </style>

.. code-block:: js

    // src/components/CounterButton.spec.ts
    import { describe, it, expect } from 'vitest'
    import { mount, flushPromises } from '@vue/test-utils'
    import CounterButton from '@/my_project/components/CounterButton.vue'

    describe('CounterButton.vue', () => {
        it('mounts and displays initial count', () => {
            const wrapper = mount(CounterButton);
            expect(wrapper.text()).toContain('Count: 0');
        });

        it('increments count on click', async () => {
            const wrapper = mount(CounterButton);
            const button = wrapper.find('button');
            await button.trigger('click');
            await flushPromises();
            expect(wrapper.text()).toContain('Count: 1');
        });
    });

Running Tests
~~~~~~~~~~~~~

Use the following npm scripts in your terminal:

.. code-block:: shell

    # Run all tests once
    npm run vitest

    # Run a specific test file
    npm run vitest -- src/components/CounterButton.spec.ts

Coverage output will appear under ``coverage/``, showing per-file metrics and highlighting untested lines.
