######################
Arches Vue Style Guide
######################

This document extends the official Vue style guide with additional conventions and best practices tailored for our projects.

Project Structure
=================

Naming Convention
~~~~~~~~~~~~~~~~~

- **Arches entity directories**  
    Use plural, lowercase names (e.g., `cards/`, `widgets/`, `reports/`)

- **Vue component directories**
    `PascalCase/` (e.g., `CustomComponent/`)

- **Non-Vue component directories**  
    `kebab-case/` (e.g., `custom-utility/`, `custom-type/`)

- **Vue components**  
    `PascalCase.vue` (e.g., `CustomComponent.vue`)

- **Utilities**  
    `kebab-case.js` or `kebab-case.ts` (e.g., `custom-utility.js`)

- **Type files**  
    `kebab-case.ts` (e.g., `custom-type.ts`)


Top-Level Structure
~~~~~~~~~~~~~~~~~~~

Top-level directories **must** align with Arches concepts (e.g., cards, widgets, reports) when such delineation is required. Otherwise, consolidate everything under a single app-level directory.


.. code-block:: shell

    # good

    src/
    └── project_name/
        ├── plugins
        ├── reports/
        │   └── CustomReport/
        │       ├── components
        │       └── CustomReport.vue
        ├── widgets
        └── types
        └── utils

    # good

    src/
    └── project_name/
        ├── components/
        │   └── CustomComponent.vue
        ├── CustomApplication.vue
        ├── types
        └── utils


Component Folder Hierarchy
~~~~~~~~~~~~~~~~~~~~~~~~~~

At every level:

- **Component files with sub-components** **must** reside in a folder named after the component.
- **Dependent components** **must** live in a `components/` subdirectory within their **parent component's** folder.
- **Shared components** (used by more than one parent) **must** be elevated to the `components/` directory at the level of the **highest parent component** that uses them.

.. code-block:: shell

    # good

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