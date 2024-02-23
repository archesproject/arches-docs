# Arches Vue Integration Styleguide

## Table of Contents

- [Purpose](#purpose)
- [Audience](#audience)
- [Basis for this Style Guide](#basis-for-this-style-guide)
- [Contributions](#contributions)
- [Integrating a Vue Component](#integrating-a-vue-component)
- [Single-Responsibility Principle and Component Decomposition](#single-responsibility-principle-and-component-decomposition)
- [Directory Structure](#directory-structure)
- [Cascading Style Sheets (CSS)](#cascading-style-sheets-css)
- [Importing Components and Component Pathing Shorthand](#importing-components-and-component-pathing-shorthand)
- [TypeScript and ESLint](#typescript-and-eslint)
- [Internationalization (i18n)](#internationalization-i18n)
- [Composition API and Single-file Components](#composition-api-and-single-file-components)
- [Testing](#testing)
- [Example Arches Vue Component Integration](#example-arches-vue-component-integration)

## Purpose

The purpose of this style guide is to establish a unified coding style and set of conventions that all contributors should adhere to when writing code for Arches. By following these guidelines, we aim to:

- Improve code readability and maintainability
- Facilitate collaboration among developers
- Enhance the overall quality and consistency of Arches software, Arches projects, and Arches applications

## Audience

This style guide is intended for developers of all levels who contribute to Arches. Whether you are a seasoned developer or a newcomer to the project, this document will provide you with the necessary guidance to write clean, consistent, and high-quality code.

## Basis for this Style Guide

This style guide for Arches is built on top of the standard Vue.js and TypeScript style guides. As such, it inherits and extends the conventions and best practices outlined in those guides. 

Any coding style, formatting, or conventions not explicitly covered in this document should be referenced from the official Vue.js and TypeScript style guides. It's important to maintain consistency with these standard guidelines to ensure compatibility and familiarity for developers working with Vue.js and TypeScript projects.

For Vue.js, you can refer to the official style guide [here](https://vuejs.org/style-guide/). Similarly, for TypeScript, you can refer to the official TypeScript style guide [here](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html).

Please consult these references for any conventions or guidelines not addressed in this style guide.

## Contributions

This style guide is a living document that evolves over time. We welcome contributions from the community to improve and expand this guide further. If you have suggestions, feedback, or would like to contribute to the style guide, please reach out to us via the [Arches Forum](https://community.archesproject.org/).

## Integrating a Vue Component

When integrating Vue-based views, plugins, or reports into the Arches framework, developers should utilize the `createVueApp` function provided at `utils/create-vue-application`. This function is specifically designed to facilitate the integration of Vue components within the Arches environment, ensuring seamless compatibility and optimal performance by abstracting interactions with the i18n API and various current and future Vue plugins, such as PrimeVue.

However, it's important to note that while the `createVueApp` function is suitable for integrating most Vue-based components, widgets require different render states and are not yet supported. As such, developers should exercise caution when attempting to integrate widgets using this function. We hope to resolve this in the near future.

Example:

```
import createVueApp from 'utils/create-vue-application';
import MyVueApplication from '@/MyVueApplication.vue';

createVueApp(MyVueApplication).then(vueApp => {
    vueApp.mount('#my-vue-application-mounting-point');
});
```

In the provided example, the createVueApp function, imported from `utils/create-vue-application`, streamlines the integration process by handling the necessary setup and configuration steps, allowing developers to focus on building the core functionality of their Vue application.

The `createVueApp` function takes a Vue component (`MyVueApplication` in this case) as its argument, representing the root component of the Vue application. This component encapsulates the entire application logic and user interface.

Once the Vue application is created using `createVueApp`, it returns a Vue application instance (`vueApp`), which can then be further manipulated or customized as needed. In the example, the `vueApp` instance is mounted to a specific element in the DOM with the mount method, using the CSS selector `#my-vue-application-mounting-point` to identify the mounting point.

## Single-Responsibility Principle and Component Decomposition

In Vue development, it's crucial to adhere to the Single Responsibility Principle (SRP) and practice component decomposition to ensure that Vue components remain maintainable and scalable. The SRP dictates that each Vue component should have a single responsibility or purpose. By focusing on doing one thing and doing it well, components become easier to understand, modify, and maintain. Following the SRP leads to more modular, reusable, and testable code. 

Component decomposition involves breaking down complex Vue components into smaller, more focused units, with each unit responsible for a specific task or feature. This practice aligns with the SRP and promotes clean, maintainable codebases.

Example:

```
<script setup>
import { ref } from 'vue';
import { User } from '@/types/User';

import UserProfileActions from '@/UserProfileActions.vue';
import UserProfileBio from '@/UserProfileBio.vue';
import UserProfileHeader from '@/UserProfileHeader.vue';

const user = ref<User>({
  name: 'John Doe',
  email: 'john@example.com',
  bio: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
});
</script>

<template>
  <div>
    <UserProfileHeader :name="user.name" :email="user.email" />
    <UserProfileBio :bio="user.bio" />
    <UserProfileActions />
  </div>
</template>
```

In this example:

- The `UserProfile` component is decomposed into three smaller components: `UserProfileHeader`, `UserProfileBio`, and `UserProfileActions`.
- Each smaller component has a specific responsibility:
    - `UserProfileHeader`: Renders the user's name and email.
    - `UserProfileBio`: Renders the user's bio.
    - `UserProfileActions`: Renders user actions (e.g., buttons for editing the profile).
- The user reactive reference is defined using ref() within the `<script setup>` block and is accessible to all components within the template.
- The `UserProfile` component integrates these smaller components directly in the template.
- By decomposing the `UserProfile` component into smaller, focused components, we achieve better maintainability and reusability in our Vue application.

## Directory Structure

A well-organized directory structure provides clarity on where to find specific files and components, making it easier for developers to navigate the codebase, understand its architecture, and make modifications efficiently. In Arches Vue applications, we utilize a non-standard directory structure to organize components. 

Example:

- src/
    - components/
        - UserProfile/
            - UserProfile.vue
            - UserProfileActions.vue
            - UserProfileBio.vue
            - UserProfileHeader.vue
        - Map/
            - Map.vue
            - MapHeader.vue
            - MapSidebar.vue
    - views
        - UserProfileView.vue
    - reports
        - MapReport.vue
    - widgets
        - MapWidget.vue

As Arches moves forward with integrating components from Vue into Knockout, we find it essential to adopt a non-standard directory structure to accommodate this scenario. For instance it's standard practice for most Vue applications to have a top-level `App.vue` file which has one or many child components that exist in the `components` directory. However since Arches will have multiple Vue applications running per project, possibly even per page, there must be some delineation between these top-level components. The pattern exemplified above illustrates a way to have such delineation while maintaining a scalable and navigable structure. Essentially, top-level components live in `views`, `reports`, `widgets`, etc, while their child components live in the `components` directory. The `components` subdirectories each contain a root component which is named the same as the subdirectory.

By utilizing this directory structure, we ensure that components from Vue can seamlessly integrate with Knockout components while maintaining clarity and organization in our codebase. 

## Cascading Style Sheets (CSS)

TBD - This will be included once PrimeVue stylesheets and theme-switching have been enabled.

## Importing Components and Component Pathing Shorthand

In Vue projects, the `@` symbol serves as a special alias that represents the root directory, typically the `src` directory. Arches is no different. This shorthand notation allows us to eliminate relative pathing and reference files or modules within the `src` directory more succinctly and consistently. 

For example, instead of specifying the relative path to a file like this:
```
import MyComponent from '../../components/MyComponent.vue';
import MyTypeScriptFunction from '../../typescript/MyTypeScriptFunction.ts';
```

We instead use @ to reference the root directory and import the file like this:
```
import MyComponent from '@/components/MyComponent.vue';
import MyTypeScriptFunction from '@/components/MyTypeScriptFunction.ts';
```

**It's important to note that Vue and TypeScript components must be imported with their file extensions (e.g., .vue or .ts).**

## TypeScript and ESLint

### Rationale

We have integrated TypeScript and ESLint linting as essential components of our Vue development environment to enhance code quality, maintainability, and developer productivity. TypeScript provides strong typing capabilities, allowing for more robust code by catching errors during development and providing better IDE support with type inference and autocompletion. ESLint, on the other hand, enforces consistent coding styles and identifies potential errors or anti-patterns in the codebase, ensuring adherence to best practices and coding standards.

### Enforcement

While this integration brings significant benefits to our Vue projects, it's important to note that newly written components will be affected by TypeScript and ESLint linting rules. Developers will need to adhere to TypeScript typing conventions and ESLint rules when writing new components to ensure consistency and compliance with the established coding standards. This enforcement takes place in the `build_development`, `build_test`, and `build_production` yarn processes. Previously written components will not be affected.

We have also added the `eslint:check`, `eslint:watch`, `ts:check`, and `ts:watch` yarn scripts.

### Separate Processes

During development, developers should run the TypeScript and ESLint `:watch` linters in separate processes to ensure efficient linting of the current project. By running these linters in separately, each process is dedicated to linting the current project or application. However, it's important to note that if you're running multiple projects or applications concurrently, you'll need a separate process for each project to ensure accurate linting results. 

For instance, if you're developing an Arches project and an Arches application, you will now likely have six concurrent processes: The project-level Django server, the project-level webpack development server, the project-level typescript watcher, the project-level eslint watcher, the application-level typescript watcher, and the application-level eslint watcher. Alternatively you could not run the eslint watcher nor the typescript watcher, and rely on the `build_development` and `build_production` for enforcement.

### Frontend dependency declaration

When adding any new frontend dependencies to your Arches project or application, it's important to declare their types in the `declarations.d.ts` file. This file serves as a central location for declaring global types and interfaces that are used across your project or application. Declaring types for frontend dependencies in `declarations.d.ts` ensures that TypeScript recognizes and understands the types provided by these modules, enabling accurate type checking and providing better IntelliSense support in your editor. 

Example:
```
# package.json
    ...
    "dependencies": {
        "foo": "0.0.1",
        ...
    }
    ...

# src/declarations.d.ts
    ...
    declare module 'foo';

```

### Referencing `this` inside Vue `<template>` tags

When accessing data properties, computed properties, or methods within a Vue component's `<template>` tags, it's essential to explicitly reference `this`. This ensures that TypeScript understands the context and correctly types the data or methods. Failing to use explicit `this` references inside `<template>` tags will result in TypeScript errors.

```
<script setup lang="ts">
const message = 'Hello, Vue!';

console.log(message)  // explicit `this` is not required when referencing in <script> tags
</script>

<template>
  <div>
    <p>{{ this.message }}</p>
  </div>
</template>
```

## Internationalization (i18n)

We utilize the vue3-gettext library for internationalization (i18n) in Vue components. This library provides a convenient way to manage translations and localization within Arches.

Below is an example code snippet demonstrating how we use vue3-gettext for i18n:

```
<script setup lang="ts">
import { useGettext } from 'vue3-gettext';
const { $gettext } = useGettext();

console.log($gettext('Foo!'))
</script>

<template>
    <h1 class="foo">{{ this.$gettext("Bar!") }}</h1>
</template>
```

In this example, we import the `useGettext` function from vue3-gettext and destructure the `$gettext` method from the returned object. We then use `$gettext` to translate strings within our template, such as "Foo!" and "Bar!". The translations are managed by vue3-gettext and the `create-vue-application` component, and are dynamically loaded based on the selected locale.

Before using internationalization features, it's important to run the following commands to extract and compile translations:

Extract Translations: Run `yarn gettext:extract` to extract translations from the source code and generate template .pot files.
Compile Translations: Run `yarn gettext:compile` to compile translated .po files into machine-readable .json files that can be used by the application.

For further information, please reference the [vue3-gettext documentation](https://github.com/jshmrtn/vue3-gettext)

## Composition API and Single-file Components

We strongly suggest utilizing the Composition API and Single-file Components for building new features or rewriting existing components into Vue.

### Composition API

The Composition API is a way of organizing and reusing logic within Vue components. It allows developers to encapsulate related logic into reusable composition functions, making it easier to manage complex component logic and share code between components.


### Single-file Components

Single-file Components are a feature of Vue that allows developers to define templates, script, and styles in a single `.vue` file. This approach promotes a more modular and cohesive structure for Vue components, making it easier to manage component-specific logic, styles, and templates in a single file. 

### Example
Here's an example of a Single-file Component that uses the Composition API, notice the <script>, <template>, and <style> tags for a component exist in the same file:

```
<script setup lang="ts">
import { ref } from 'vue';

const count = ref(0);
const increment = () => {
  count.value++;
};
</script>

<template>
  <button @click="this.increment">Increment</button>
  <p class="counter">Count: {{ this.count }}</p>
</template>

<style scoped>
.counter {
    color: red;
}
</style>

```

## Testing

TBD - This will be included once a testing pattern has been explored.

## Example Arches Vue Component Integration

Below is an example of creating a new plugin for Arches. This example includes import patterns, TypeScript patterns, internationalization, the composition API, single-file components, and Vue/Knockout integration

```
// media/js/views/components/plugins/my-plugin.js

import ko from 'knockout';
import MyPlugin from '@/plugins/MyPlugin.vue';
import createVueApp from 'utils/create-vue-application';
import MyPluginTemplate from 'templates/views/components/plugins/my-plugin.htm';


ko.components.register('my-plugin', {
    viewModel: function() {
        createVueApp(MyPlugin).then(vueApp => {
            vueApp.mount('#my-plugin-mounting-point');
        });
    },
    template: MyPluginTemplate,
});

```

```
// templates/views/components/plugins/my-plugin.htm

<div id="my-plugin-mounting-point"></div>
```

```
// src/plugins/MyPlugin.vue

<script setup lang="ts">
import { useGettext } from 'vue3-gettext';
const { $gettext } = useGettext();

console.log($gettext('Foo!'))
</script>

<template>
    <h1 class="foo">{{ this.$gettext("Bar!") }}</h1>
</template>

<style scoped>
.foo {
    color: red;
}
</style>
```