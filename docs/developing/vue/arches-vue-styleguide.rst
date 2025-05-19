######################
Arches Vue Style Guide
######################

Table of Contents
=================

- `Purpose`_
- `Basis for Style Guide`_
- `Contributions`_
- `Frontend Structure`_
    - `File and Folder Naming Conventions`_
    - `Top-Level Structure`_
    - `Component Folder Hierarchy`_
- `Component Structure`_
    - `Single-File Components`_
    - `Component Decomposition`_
    - `Passing Data`_
        - `Fetch Proximity`_
        - `Primitives First`_
        - `Derived State`_
        - `Event Emission`_
        - `Slots`_
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
- For TypeScript, you can refer to the `official TypeScript style guide <https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html>`_.

Contributions
=============

This style guide is a living document that evolves over time. We welcome contributions from the community to improve and expand this guide further. If you have suggestions, feedback, or would like to contribute to the style guide, please reach out to us via the `Arches Forum <https://community.archesproject.org/>`_.

Frontend Structure
==================

File and Folder Naming Conventions
----------------------------------

- **Arches entity directories**
    - Use plural, lowercase names to reflect domain concepts.  
    - e.g. ``cards/``, ``widgets/``, ``reports/``

- **Vue component directories**
    - One folder per component, named in PascalCase.  
    - e.g. ``CustomComponent/``

- **Non-Vue component directories**
    - Utility or helper folders in kebab-case.  
    - e.g. ``custom-utility/``, ``date-utils/``

- **Vue components**
    - File names in PascalCase with a ``.vue`` extension.  
    - e.g. ``UserCard.vue``, ``MapViewer.vue``

- **Utilities & helpers** 
    - Use kebab-case, file extension ``.js`` or ``.ts``.  
    - e.g. ``fetch-api.ts``, ``format-date.js``

- **Type files** 
    - Single-purpose type definitions in kebab-case, ``.ts``.  
    - e.g. ``user-profile.ts``, ``map-types.ts``

Top-Level Structure
-------------------

- Top-level directories **must** align with Arches concepts (e.g., cards, widgets, reports) when such delineation is required. Otherwise, consolidate everything under a single app-level directory.

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

- **Why?**
    - **Standardization**: Consistent naming and structure make it easier for developers to navigate the codebase.
    - **Organization**: Grouping related components together makes it easier to find and manage them.

Component Folder Hierarchy
--------------------------

- At every level:
    - **Component files with sub-components** **must** reside in a folder named after the component.
    - **Dependent components** **must** live in a `components/` subdirectory within their **parent component's** folder.
    - **Shared components** (used by more than one parent) **must** be elevated to the `components/` directory at the level of the **highest parent component** that uses them.

    .. code-block:: shell

        src/
        └── project_name/
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

- **Why?**
    - **Clarity**: Each component's folder contains everything it needs, making it easier to understand and navigate.
    - **Encapsulation**: Keeps related components together, reducing the risk of naming conflicts and improving modularity.

Component Structure
===================

Single-File Components
----------------------

- Single-File Components (SFCs) are the preferred way to define Vue components. 

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

- **Why?**
    - **Encapsulation**: All component-related code is in one place, making it easier to understand and maintain.
    - **Separation of concerns**: Each section (template, script, style) has its own purpose, improving readability.

Component Decomposition
-----------------------

- Components should be decomposed into smaller, reusable components whenever possible. Aim for a single responsibility per component.

    .. code-block:: shell

        src/
        └── project_name/
            └── widgets/
            └── CustomWidget/
                ├── components/
                │   ├── CustomWidgetEditor.vue
                │   └── CustomWidgetViewer.vue
                └── CustomWidget.vue

- **Why?**
    - **Reusability**: Smaller components can be reused in different contexts, reducing code duplication.
    - **Maintainability**: Easier to understand and modify smaller components than large monolithic ones.
    - **Testing**: Smaller components are easier to test in isolation.

Passing Data
------------

- **Fetch Proximity**
    - Fetch data in the component that actually renders it. Don't lift network calls higher than needed.

    .. code-block:: vue

        <!-- Bad: fetching at a high-level parent when only the table needs it -->

        <!-- Dashboard.vue -->
        <script setup lang="ts">
        import { ref, watchEffect } from 'vue';
        import UserTable from '@/my_project/Dashboard/components/UserTable.vue';
        import type { User } from '@/my_project/types.ts';

        const users = ref<User[]>([]);
        watchEffect(async () => {
            users.value = await fetch('/api/users').then(resp => resp.json());
        });
        </script>

        <template>
            <div class="dashboard">
                <UserTable :users="users" />
            </div>
        </template>

    .. code-block:: vue

        <!-- Good: fetching as close as possible to where data is rendered -->

        <!-- Dashboard.vue -->
        <script setup lang="ts">
        // Parent no longer fetches users
        </script>

        <template>
            <div class="dashboard">
                <UserTable />
            </div>
        </template>


        <!-- UserTable.vue -->
        <script setup lang="ts">
        import { ref, watchEffect } from 'vue';
        import type { User } from '@/my_project/types.ts';

        const users = ref<User[]>([]);
        watchEffect(async () => {
            users.value = await fetch('/api/users').then(resp => resp.json());
        });
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
      
    - **Why?** 
        - **Encapsulation**: Data-fetch logic lives alongside the view that consumes it.  
        - **Limited prop drilling**: Minimizes passing data through unrelated parents.   
        - **Error isolation**: Failures are handled locally, without cascading side effects.  

- **Primitives First**
    - Pass simple values (strings, numbers, booleans, small arrays/objects) instead of entire model objects whenever possible.

    .. code-block:: vue

        <!-- Bad: passing entire model objects -->
        <UserProfile :user="currentUser" />

        <!-- Good: passing only primitive values -->
        <UserProfile
            :user-id="currentUser.id"
            :user-name="currentUser.name"
            :is-admin="currentUser.isAdmin"
        />
    
    - **Why?** 
        - **Explicit API**: Readers, tools, and developers see exactly which fields the component needs.  
        - **Immutable flow**: Primitives can't be mutated in place, preserving one-way data flow.  
        - **Efficient updates**: Changes to unused object properties won't force re-renders.  

- **Derived State**
    - If a component's sole responsibility is to derive or summarize data pass the raw data and let it compute internally.

    .. code-block:: vue

        <script setup lang="ts">
        import { ref, computed, watchEffect } from 'vue';
        import OrderSummary from '@/my_project/OrderSummary.vue';
        import type { Order } from '@/my_project/types.ts';

        // Raw data fetched here
        const orders = ref<Order[]>([]);
        watchEffect(async () => {
            orders.value = await fetch('/api/orders').then(response => response.json());
        });
        </script>

        <template>
            <!-- OrderSummary receives the full list and does its own computing -->
            <OrderSummary :orders="orders" />
        </template>

    - When multiple children need the same computed value, derive once in the parent and pass primitives to avoid duplication and ensure consistency.

    .. code-block:: vue

        <script setup lang="ts">
        import { ref, computed, watchEffect } from 'vue';
        import OrderSummary from '@/my_project/OrderSummary.vue';
        import OrderDetails from '@/my_project/OrderDetails.vue';
        import type { Order } from '@/my_project/types.ts';

        // Raw data fetched here
        const orders = ref<Order[]>([]);
        watchEffect(async () => {
            orders.value = await fetch('/api/orders').then(response => response.json());
        });

        // Derived state: compute once in the parent
        const totalOrders = computed(() => orders.value.length);
        </script>

        <template>
            <!-- Pass the computed value to both children -->
            <OrderSummary :total-orders="totalOrders" />
            <OrderDetails :total-orders="totalOrders" />
        </template>

    - **Why?**  
        - **Performance**: Avoids recomputing derived values in multiple components.
        - **Predictable props**: Child components receive only the exact values they need.  
        - **Consistency**: Ensures every consumer uses the same computed values, preventing drift. 

- **Event Emission** 
    - Emit semantic events (kebab-case) with typed payloads:

    .. code-block:: vue

        <script setup lang="ts">
        interface RowSelectedEvent { rowId: number }

        defineEmits<{
            (e: 'row-selected', payload: RowSelectedEvent): void
        }>();

        function onRowClick(id: number) {
            emit('row-selected', { rowId: id });
        }
        </script>

    - **Why?**  
        - **Explicit contracts**: Consumers know exactly what events to expect and how to handle them.  
        - **Type safety**: TypeScript ensures the payload matches the expected structure.  

- **Slots**
    - Use scoped slots for maximum flexibility; name them clearly to indicate their purpose.

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

    - **Why?**  
        - **Flexibility**: Consumers can customize the rendering of specific parts of the component.  
        - **Separation of concerns**: Slots allow for a clear distinction between the component's structure and its content.  

The `<script>` Tag
==================

This block defines a component's logic. Follow these rules for clarity, consistency, and maintainability.

Coding Standards
----------------

- **Script Scope**
    - All component logic must be declared inside <script setup>, and <script setup> should always have typescript as the defined language.

    .. code-block:: vue

        <!-- Good: scoped to component, using typescript -->
        <script setup lang="ts">
        import { ref } from 'vue';

        const count = ref(0);
        function incrementCount() { count.value++ }
        </script>

        <!-- Bad: global scope pollution, no typescript -->
        <script>
            const count = 0;
            function incrementCount() { count++; }
        </script>

    - **Why?**
        - **TypeScript support**: Enables full TypeScript support directly within each component.
        - **Scope safety**: All variables and functions are scoped to the component, preventing accidental global pollution.

- **Function Declarations**
    - Use named `function` declarations for component methods; **do not** use anonymous/arrow functions or function expressions.
    - Use of anonymous/arrow functions is allowed for inline callbacks (e.g., `setTimeout`, `Promise.then`, `filter`, `onMounted`, `computed`, etc.).

    .. code-block:: js

        <!-- Bad: arrow function for component method -->
        const incrementCount = () => { count.value++ };

        <!-- Bad: function declaration for component method -->
        const incrementCount = function() { count.value++ };

        <!-- Good: named function declaration for component method -->
        function incrementCount() { count.value++ }

        <!-- Good: arrow function used for inline callback -->
        setTimeout(() => { count.value++ }, 1000);

    - **Why?**
        - **Hoisting**: Named functions are hoisted, allowing them to be called before their declaration in the code. This can help avoid issues with function order and improve readability.
        - **Debugging**: Named functions provide better stack traces and error

- **Constants & Literals**
    - Declare fixed values in `SCREAMING_SNAKE_CASE`.  
    - Declare all string literals and magic numbers as named constants.

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

    - **Why?**
        - **Readability**: Named constants make the code more self-explanatory and easier to understand and debug.
        - **Maintainability**: Changing a single constant is easier than searching for all occurrences of a magic number or string literal.

- **Naming Conventions**
    - Use descriptive identifiers; avoid single-letter names.

    .. code-block:: js

        // Bad: single-letter naming
        function doubleValue(x) { return x * 2; }

        // Good: descriptive naming
        function doubleValue(value) { return value * 2; }

    - **Why?**
        - **Clarity**: Descriptive names provide context and meaning, making the code easier to read and understand.
        - **Maintainability**: Clear names help future developers (or yourself) quickly grasp the purpose of variables and functions.

- **Modularity & Reuse**
    - Extract non-UI logic (data transformations, business rules) into composables or utility modules.  

    .. code-block:: js

        // Bad: non-UI logic in component
        function calculateDiscount(price, discount) {
            return price - (price * discount);
        }

        // Good: non-UI logic in utility module
        import { calculateDiscount } from '@/my_project/utils/discounts.ts';

    - **Why?**
        - **Separation of concerns**: Keeps UI logic separate from business logic, making components easier to read and maintain.
        - **Reusability**: Composables and utility modules can be reused across multiple components, reducing code duplication.

- **Side-Effects & Async Handling**
    - Avoid performing side-effects (API calls, timers, storage access, data formatting, etc.) at module import in <script>.
        - Trigger them inside lifecycle hooks (e.g. onMounted, onBeforeUnmount) or within reactive effect functions (e.g. watchEffect, computed).

    - Always wrap your async/await operations in try/catch, handle errors explicitly, and ensure failures are surfaced to the UI or calling code.

    .. code-block:: vue

        <script setup lang="ts">

        const count = ref(0);
        function incrementCount() { count.value++ }

        <!-- Bad: module scope side-effects -->
        incrementCount(); // This runs immediately when the module is loaded

        <!-- Good: side-effects in lifecycle hooks -->
        onMounted(() => {
            incrementCount();
        });
        </script>

    - **Why?**
        - **Predictability**: Side-effects should only occur in controlled environments (e.g. lifecycle hooks) to avoid unexpected behavior.
        - **Error handling**: Wrapping async operations in try/catch allows for graceful error handling and user feedback.

- **Type Safety**
    - Import and use explicit types; avoid use of the `any` type. Annotate all function return types.

    .. code-block:: js

        // Bad: using any type
        function fetchData(): any {
            return fetch('/api/data').then(response => response.json());
        }

        // Good: explicit type annotation
        interface User {
            id: number;
            name: string;
        }

        function fetchData(): Promise<User[]> {
            return fetch('/api/data').then(response => response.json());
        }

    - **Why?**
        - **Type safety**: Using explicit types helps catch errors at compile time, reducing runtime issues.
        - **Documentation**: Type annotations serve as documentation for function behavior and expected input/output.

Import Pathing
--------------

- **Use project alias** (`@/…`) for all local imports; avoid raw relative paths. e.g. 

    .. code-block:: js

        // Bad: raw relative path
        import { fetchData } from '../../utils/fetch-data.ts';
        
        // Good: project alias
        import { fetchData } from '@/project_name/utils/fetch-data.ts';

- **Why?**
    - **Readability**: Project aliases make it clear where the module is located without needing to trace relative paths.
    - **Maintainability**: Avoids issues with deep nesting and makes it easier to refactor or reorganize the project structure.

Import Order
------------

- Import lines should be grouped and ordered as follows:
    1. **Vue core**  
    2. **Third-party modules**  
    3. **Third-party Vue components**  
    4. **External Arches Vue components**
    5. **Local Vue components**  
    6. **External Arches utilities/composables**
    7. **Local utilities/composables**  
    8. **Third-party types**  
    9. **External Arches types**
    10. **Local types**  

.. code-block:: vue

    <script setup lang="ts">
    // 1. Vue core
    import { ref, computed } from 'vue';

    // 2. Third-party modules
    import { useGettext } from 'vue3-gettext';

    // 3. Third-party Vue components
    import { ProgressSpinner } from 'primevue/progressspinner';

    // 4. External Arches Vue components
    import ExternalComponent from '@/external_project/ExternalComponent.vue';

    // 5. Local Vue components
    import MyComponent from '@/project_name/components/MyComponent.vue';

    // 6. External Arches utilities/composables
    import { doSomeBusinessLogic } from '@/external_project/utils/do-some-business-logic.ts';

    // 7. Local utilities/composables
    import { fetchData } from '@/project_name/utils/fetch-data.ts';

    // 8. Third-party types
    import type { Component } from 'vue';

    // 9. External Arches types
    import type { ExternalType } from '@/external_project/types.ts';

    // 10. Local types
    import type { UserProfile } from '@/project_name/types.ts';

    // Your component logic here
    </script>

Declaration Order
-----------------

- Within your `<script setup>` block, organize declarations in this sequence.
    1. **`defineProps`**  
    2. **`defineExpose`/`defineEmits`**  
    3. **Set up composables/utilities**
    4. **Dependency injection**
    5. **Constants & configuration**
    6. **Reactive state**
    7. **Computed properties**  
    8. **Watchers**  
    9. **Lifecycle hooks** 
    10. **Methods/functions**  

.. code-block:: vue

    <script setup lang="ts">
    import { ref, computed, watch, onMounted, inject } from 'vue';
    import { useGettext } from 'vue3-gettext';
    import type { Item } from '@/project_name/types';

    // 1. defineProps
    const props = defineProps<{ id: number }>();

    // 2. defineExpose/defineEmits
    defineExpose({ myMethod: myMethod });
    const emit = defineEmits<{ (e: 'loaded'): void }>();

    // 3. Set up composables/utilities
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

    // 8. Watchers
    watch(() => props.id, myFunction, { immediate: true });

    // 9. Lifecycle hooks
    onMounted(() => {
        myFunction();
    });

    // 10. Methods/functions
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

The `<template>` Tag
====================

Defines the component's UI. Keep templates clear, consistent, and easy to scan.

Attribute Ordering & Formatting
-------------------------------

- When declaring attributes in your `<template>`, group and order them as follows. Within each group, sort attributes alphabetically.
    1. **Directives** (e.g. `v-for`, `v-if`)  
    2. **Slots** (e.g. `v-slot:header="…"` )
    3. **Static attributes** (e.g. `id`, `class`)  
    4. **Dynamic props** (e.g. `:prop="…"` )  
    5. **Event listeners** (e.g. `@click="…"` )  
    6. **Modifiers** (e.g. `@click.prevent="…"` )  

- Formatting rules:
    - **Inline vs. Multiline**  
        - **One attribute**: keep on the same line as the tag.  
        - **Multiple attributes**: one per line, indented under the tag.  
    - **Explicit assignment**  
        - Always write `prop="value"` or `:prop="value"`.  
        - Do **not** use shorthand (`:prop` without value) or omit values.  
    - **Kebab-case**  
        - All attribute names (including custom props and events) **must** use kebab-case.

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

- **Why?**
    - **Readability**: Consistent ordering and formatting make it easier to scan and understand the template.
    - **Maintainability**: Clear structure helps future developers (or yourself) quickly grasp the component's purpose and behavior.

Self-Closing Tags
-----------------

- Use self-closing syntax for elements or components without children:

.. code-block:: vue

    <template>
        <LogoIcon />
        <img src="@/assets/logo.png" alt="Logo" />
    </template>

- **Why?**
    - **Clarity**: Self-closing tags clearly indicate that the element has no children, improving readability.
    - **Consistency**: Using self-closing syntax for void elements (e.g., `<img>`, `<input>`) maintains a consistent style throughout the codebase.

Logic in Templates
------------------

- **No complex logic**  
    - Avoid ternaries, chained method calls, or heavy expressions.  
    - Move conditions and transformations into `computed` or methods.  

.. code-block:: vue

    <!-- Good: simple v-if, logic lives in computed -->
    <template>
        <div v-if="isVisible">{{ displayText }}</div>
    </template>

    <!-- Bad: inline ternary and method call -->
    <template>
        <div>{{ isVisible ? formatText(user.name) : '—' }}</div>
    </template>

- **Why?**
    - **Readability**: Templates should be easy to read and understand at a glance.  
    - **Performance**: Heavy computations in templates can lead to unnecessary re-renders and performance issues.

Text in Templates
-----------------

- **Internationalization**  
    - Wrap all user-facing strings with `$gettext()`.  
    - Never concatenate translated strings together; use placeholders instead.

- **No loose text nodes**  
    - Surround plain text with an inline element (e.g., `<span>`) or semantic tag.  

.. code-block:: vue

    <!-- Bad: unwrapped text node, string concatination, some strings without i18n -->
    <template>
        <div>
            {{ $gettext('Hello,') }}{{ user.name }}!

            <Button @click="handleClick">
                Click me!
            </Button>
        </div>
    </template>

    <!-- Good: wrapped text node, placeholders instead of concatination, all strings have i18n -->
    <template>
        <div>
            <span>{{ $gettext('Hello, %{user.name}!') }}</span>
            
            <Button @click="handleClick">
                {{ $gettext('Click me!') }}
            </Button>
        </div>
    </template>

- **Why?**
    - **Internationalization**: Correctly wrapping strings with `$gettext()` ensures they are translatable and can be easily localized.
    - **Semantic HTML**: Using inline elements or semantic tags improves accessibility and SEO by providing context to screen readers and search engines.

The `<style>` Tag
=================

Defines component-scoped CSS. Follow these rules for responsive, maintainable, and themeable styles.

Scope
-----

- **Scoped styles**  
    - Prefer to use `<style scoped>` to ensure styles are applied only to the component.  
    - Reserve global styles and design tokens for your global CSS or theme files unless absolutely necessary.

.. code-block:: vue

    <!-- Bad: global styles -->
    <style>
        .header {
            color: var(--theme-primary);
        }
    </style>

    <!-- Good: scoped styles -->
    <style scoped>
        .header {
            color: var(--theme-primary);
        }
    </style>

- **Why?**
    - **Isolation**: Scoped styles prevent unintended side effects on other components, ensuring consistent styling.
    - **Maintainability**: Changes to a component's styles won't affect other components, reducing the risk of introducing undesired behavior.

Layout Patterns
---------------

- **Flexbox & Grid only**  
    - Use `display: flex` for one-dimensional layouts and `display: grid` for two-dimensional arrangements.  
- **Use `gap`**  
    - Space items with `gap`; do **not** rely on margins for core layout.  
- **No legacy hacks**  
    - Never use `float`, `inline-block`, or other outdated techniques.
- **Single-line vs multi-line selectors**
    - Use single-line selectors for enforcing exactly one style rule.
    - Use multi-line selectors for grouping multiple rules together.

.. code-block:: vue

    <style scoped>

        /* Bad: single-line selector for multiple rules */
        .item { display: flex; gap: 1rem; }

        /* Good: single-line selector for one rule */
        .item { display: flex; }

        /* Good: multi-line selector for multiple rules */
        .item {
            display: flex;
            gap: 1rem;
        }
    </style>

- **Why?**
    - **Flexibility**: Flexbox and Grid provide powerful layout capabilities for modern web applications.
    - **Maintainability**: Using `gap` simplifies spacing management and reduces the need for complex margin calculations.

Units & Sizing
--------------

- **`rem` for nearly everything**  
    - Use `rem` units for spacing, typography, gaps, borders, and other dimensional values.

- **Viewport units sparingly**  
    - Reserve `vh`/`vw` for elements that must span the viewport (e.g., full-screen sections or modals).

- **Percentages for fluid layouts**  
    - Apply `%` when you need relative sizing (e.g., fluid widths in responsive grids).

- **No `px`**  
    - Avoid `px` units entirely to ensure scalability, accessibility, and consistent theming.

.. code-block:: css

    /* Bad: using px units */
    .container { width: 800px; padding: 20px; }

    /* Good: using rem units */
    .container { width: 50rem; padding: 1.25rem; }

    /* Good: using percentage for fluid layout */
    .container { width: 100%; }

- **Why?**
    - **Scalability**: Using `rem` and `%` units allows for better scaling across different screen sizes and resolutions.
    - **Accessibility**: Relative units ensure that text and elements can be resized according to user preferences, improving accessibility.

Offsets & Positioning
---------------------
- **No hard-coding single-side offsets**  
    - Instead of using `margin-left`, `margin-top`, etc., use logical properties like `margin-inline-start` and `margin-block-start`.

- **No negative margins**  
    - Negative `margin-*` values are forbidden.

.. code-block:: vue

    <style scoped>
        /* Bad: negative margin, not using logical properties */
        .container .item { margin-left: -1rem; }

        /* Good: no negative margin, using logical properties */
        .container { padding-inline-start: 1rem; }
        .item { margin-inline-start: 0; }
    </style>

- **Why?**
    - **Logical properties**: Using logical properties ensures consistent behavior across different language displays (e.g. left-to-right vs. right-to-left).
    - **Avoiding layout shifts**: Negative margins can lead to unexpected layout shifts and make it harder to maintain a consistent design.

No `calc()`
-----------

- The `calc()` function is forbidden in component styles.

.. code-block:: css

    /* Bad: using calc() */
    .container { width: calc(100% - 2rem); }

    /* Good: using rem units */
    .container { width: 50rem; }

- **Why?**  
    - It complicates the CSS and makes it harder to read.  
    - It can cause unexpected layout shifts, especially in responsive designs.

Theming & Colors
----------------

- **Design Tokens Only**  
    - Always reference your design tokens instead of raw values. 

- **Centralize & Document**  
    - Keep all tokens (colors, typography scales, breakpoints, etc.) in a single theme file.

- **Semantic Layers**  
    - Build on top of raw palette entries with semantic tokens (e.g. ``--color-success``) so UI intent drives your choices.

- **Light/Dark Support**  
    - Define variants for both modes in your theme preset.

.. code-block:: js

    import { definePreset } from '@primevue/themes';
    import { DEFAULT_THEME } from "@/arches/themes/default.ts";

    export const MyTheme = definePreset(DEFAULT_THEME, {
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

- **Why?**
    - **Consistency**: Using design tokens ensures a consistent look and feel across the application.
    - **Maintainability**: Centralizing tokens makes it easier to update and manage styles.

Selector Naming
---------------

- **Dot-delineated hierarchy**  
    - Prefix selectors with the component's root class, then chain child class names:

.. code-block:: css

    <style scoped>
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
            color: var(--theme-primary);
        }
    </style>

- **Why?**
    - **Clarity**: Dot-delineated selectors make it clear which component the styles belong to, improving readability.
    - **Avoiding conflicts**: Using a unique prefix reduces the risk of style conflicts with other components.

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

- **Why?**
    - **Organization**: Grouping tests by component or utility helps maintain a clean project structure.
    - **Ease of navigation**: Developers can quickly locate tests related to a specific component or utility without searching through a separate test directory.

Writing Frontend Tests
----------------------

When crafting your tests, adhere to these best practices:

- **Isolation**  
    - Mount each component on its own—stub or mock child components to pinpoint issues precisely.

- **Coverage**  
    - Cover all code paths, including edge cases (error states, conditional rendering, emitted events).

- **Readability**  
    - Use clear, descriptive test names and group related tests with ``describe`` blocks.

- **Async Handling**  
    - Use ``flushPromises`` or ``await nextTick()`` after triggering asynchronous updates.

- **Cleanup**  
    - Unmount or destroy wrappers if they persist between tests (though Vitest's JSDOM resets per test by default).

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

- **Why?**
    - **Isolation**: Testing components in isolation helps identify issues more easily and ensures that tests are not affected by other components.
    - **Readability**: Clear and descriptive test names make it easier for developers to understand the purpose of each test.
    - **Maintainability**: Well-structured tests are easier to maintain and update as the codebase evolves.

Running Frontend Tests
----------------------

- Use the following npm scripts in your terminal:
    - Coverage output will appear under ``coverage/``, showing per-file metrics and highlighting untested lines.

.. code-block:: shell

    # Run all tests once
    npm run vitest

    # Run a specific test file
    npm run vitest -- src/components/CounterButton.spec.ts
