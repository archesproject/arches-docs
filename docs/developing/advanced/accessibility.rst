#############
Accessibility
#############

As of version 7.5, Arches can be configured to meet `WCAG <https://www.w3.org/WAI/standards-guidelines/wcag/>`_ defined **AA** level accessibility requirements for all public facing user interfaces. Please review te documentation on activating the Arches :ref:`Accessibility Mode`.

Please continue reading below to understand how to better meet accessibility requirements for your customization of Arches.

Contents
========

* `Summary`_
* `Tools Used`_
* `Key Points`_
    * `Color Contrast`_
    * `Form Fields`_
    * `Headings`_
    * `Links`_
    * `Keyboard`_
    * `Responsive Design`_
    * `HTML Validation`_
    * `Screen Reader`_
* `Alternative solutions where components cannot be made accessible`_
* `Additional Points`_

Summary
=======

It is important that Arches is developed with inclusivity in mind by making it accessible to users with disabilities.

In a number of regions, organisations are required to ensure that any software they use, or provide as a service, is accessible for users with disabilities. To this end, any UI development within Arches must take measures to conform to the guidance set out in the WCAG 2.1 requirements. This will allow Arches to be more easily adopted by such organisations and provide benefits to a wider audience.

The following information details the minimum steps required adhere to WCAG accessibility guidelines. Although the remit has been to adhere to AA standards, wherever possible AAA has been reached for issues such as color contrast.

Here's a link to all the `WCAG 2.1 requirements <https://www.w3.org/TR/WCAG21/#requirements-for-wcag-2-1>`_

You should ensure that you have developed and tested any code against these as a minimum when submitting code back to the project.

Tools Used
==========

* Browsers - Chrome, Firefox and Safari (on iOS via Browserstack)
* Browser extensions (all free, no sign-up required apart from Browserstack):

    * `Wave <https://wave.webaim.org/>`_
    * `Lighthouse <https://developers.google.com/web/tools/lighthouse/>`_
    * `Browserstack <https://www.browserstack.com/>`_ - requires paid subscription
    * `Landmarks <https://chrome.google.com/webstore/detail/landmark-navigation-via-k/ddpokpbjopmeeiiolheejjpkonlkklgp?hl=en-GB>`_
    * `NVDA <https://www.nvaccess.org/>`_
    * `W3C HTML Validator <https://validator.w3.org/>`_
    * `Contrast checker <https://webaim.org/resources/contrastchecker/>`_

Key Points
==========

Although many files have been worked on for the many different requirements, there have been some frequently identified issues. Here are the commonly found problems:

Color Contrast
--------------

.. note:: Tools used: `Wave`_ / `Contrast checker`_

Using a combination of the Wave browser extension and the Contrast Checker website mentioned above, you can identify what elements on a page that need changing, for example, from the Arches v5 demo site, take the "Resource Type" button on the search page:

It has a background color ``#579DDB`` and a foreground color ``#FFFFFF`` - this fails the contrast test. You can use the contrast checker to test how things look when you lighten or darken either the background or foreground. In this instance, using the slider, lets darken the background color to be ``#1E5A8F`` instead, which passes WCAG AAA.

Form Fields
-----------

.. note:: Tools used: `Wave`_ / `Lighthouse`_ / `W3C HTML Validator`_ / `NVDA`_

Ensure form fields have correct labelling.

For example, instead of:

    .. code-block:: html

        <h5>Field label text</h5>
        <input type="text">

use this code instead:

    .. code-block:: html

        <label for="myField">Field label text</label>
        <input type="text" id="myField">

Sometimes it may suit design purposes not to have a label and make use of placeholder text. This is fine but be mindful that users using screen readers will not get placeholder text read out to them. So we can make use of the ``aria-label`` attribute:

    .. code-block:: html

        <input type="text" id="myField" placeholder="Field label text" aria-label="Field label text">

...or using ``aria-labelledby``:

    .. code-block:: html

        <span id="someText">Field label text</span>
        <input type="text" aria-labelledby="someText">

Also, you can use the aria-label attribute to place in a container element to describe what content is within:

    .. code-block:: html

        <div class="container" aria-label="Search buttons to filter the search results">
            <button id="filterBtn">Filters</button>
            <button id="typeBtn">Type</button>
        </div>

Headings
--------

.. note:: Tools used: `Wave`_ / `Landmarks`_

Make sure that all headings are ordered and nested correctly. There should only be one ``<h1>`` tag per page and be sure to not any skip heading levels, so the correct order should be something like this:

.. code-block:: html

    <h1>Main Heading</h1>
    <h2>Navigation Menu</h2>
    <h2>Sidebar</h2>
        <h3>Profile</h3>
        <h3>Settings</h3>
        <h3>Help</h3>
        ...

Links
-----

.. note:: Tools used: `Wave`_ / `W3C HTML Validator`_

If a link contains no text, then the function or purpose will not be understood by screen reader users.

For example:

.. code-block:: html

    <a href="">View more...</a>
    or
    <a>View more...</a>

...should be:

.. code-block:: html

    <a href="#" aria-label="View more search results">View more...</a>

...note the use of an ``aria-label`` to provide a clearer description of what the link is for.

Keyboard
--------

.. note:: Tools used: none (manual checks required)

UI development must ensure the website/page is still navigable and actionable via the keyboard. There may be instances where click events are required on elements other an ``href`` links, for example (using Knockout binding):

.. code-block:: html

    <div class="css-class" data-bind="click: function() {myFunc();}">
        Some content
    </div>

This will listen for a mouse click on the ``div`` element but this won't work if a user is using their keyboard to navigate and operate the website. A keyboard user will not be able to ``tab`` to this element or be able to action it by pressing their space bar or enter key. To facilitate this, we need to make it ``tabbable`` and actionable via a ``keypress`` as follows:

.. code-block:: html

    <div class="css-class"
        tabindex="0"
        data-bind="click: function() {myFunc();}"
        onkeypress="$(this).trigger('click');">
        Some content
    </div>

Note the use of ``tabindex="0"`` which includes the element within the natural DOM tab order and the ``onkeypress`` which in this example uses jQuery to force a ``click``. There may be several ways to achieve this but always ensure any clickable element can also be actioned using a keyboard, usually the enter key once tabbed to.

Responsive Design
-----------------

.. note:: Tools used: `Lighthouse`_ / `Browserstack`_ / Browsers (Chrome, Firefox and Safari)

When designing websites, we must think about all users and not for example, only desktop or laptop users with large screens. Users with visual impairment may increase the font size or spacing, or possibly the screen resolution may be lower.

By developing a responsive application, users making these adjustments will benefit from the application adjusting correctly to it. The application will also benefit from this by being available on tablets and mobile devices and in some regions, mobile phones are peoples' only computing device.

The website should offer the same functionality whether viewing on a large monitor or mobile screen and anything in between so that we can be as inclusive as possible. If certain information cannot be viewed on a smaller screens, then a suitable alternative should be presented to the user.

Arches uses the javascript library called Bootstrap which enables the content to be rendered in a grid system that can be adapted to suit varying screen sizes and types, including mobiles and tablets. No content should appear 'cut-off' when reducing the screen width, it should either stack, wrap or be presented differently.

This can easily be tested in a browser such as Chrome or Firefox which have built in developer tools for viewing at different devices or screen widths. Of course the ultimate test would be to use an actual device to see what happens in the real world, for this level of testing I would recommend Browserstack which has access to many different physical devices and browsers.

It's also good practice to ensure that web pages operate the same using different web browsers, for example some things may not work correctly in Safari or Chrome but everything seems fine in Firefox.

HTML Validation
---------------

.. note:: Tools used: `W3C HTML Validator`_

Any rendered ``html`` needs to pass `W3C HTML Validator`_  tests. With any dynamically produced web page, it's easy to load the page in a browser and view the source, copy and paste into the 'Validate by direct input' form field, run the test and work on any errors as necessary.

Here are some common issues found:

* Empty id and class attributes, like ``id=""`` and ``class=""`` - if they're empty remove them
* Incorrect html markup, like having a div tag inside a span tag
* Incorrect html5 semantic markup - for example no landmarks, no header, no main, no footer etc
* On some pages, the first code on a page contains the open source copyright comment, which is acceptable and required by the GNU Affero General Public License, but sometimes the comment is duplicated causing a validation error

Screen Reader
-------------

Always be mindful of users that require to use screen readers and check how sections of the page are read out and in what order.

For desktop checks, use the `NVDA`_ application to identify possible changes or where to include some ``aria-label`` descriptive text to assist with the content visualisation.

Mobile devices have some built in screen reader technology, for iOS it's called **Voice Over** and can be accessed under ``Settings>Accessibility``. For Android devices it's called **Screen Reader** and can be accessed via ``Settings>Accessibility>Screen reader``.

For example, when viewing a web page, one of the first things read out may be the menu. If the menu has many items, this could become a tedious activity, so it's good practice to include a "Skip to main content" link that appears when a user first presses the tab button, pressing enter should change focus to the start of the main content, bypassing the menu items.

Alternative solutions where components cannot be made accessible
================================================================

In the event that a specific component cannot be made fully accessible, an alternative method of achieving the same outcome should be provided.

For example, if using an SVG canvass type library to display information or provide a search function, a tabular alternative could also be created that provides the same function.

Ideally, the accessible solution would be the primary solution.

Additional Points
=================

There are many more WCAG guidelines that need to be adhered to but these mentioned here are among the most common. It's always good practice to have these points in mind whenever creating web pages/content. Always keep in mind how a keyboard only user would be able to interact with pages and how they would still work on smaller devices such as tablets or mobiles.

Even though your targeted users may not be using mobile devices, you have to cater for every need. In this day and age, the **"Mobile first"** principle should be used and play a significant role in any product design/development work.
