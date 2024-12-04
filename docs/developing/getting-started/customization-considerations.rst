###################################
Arches Customization Considerations
###################################

If you are leading a project or organization considering customizing Arches software, please read this document carefully. Customization is an inherently risky endeavor, especially if you need to maintain and support your information systems over multiple years.

The practices described here will reduce costs, reduce long term maintenance and security risks, and will lead to greater impact, enhanced sustainability, and open doors for future opportunities. That said, to maximize sustainability, security, maintainability, quality and impact, it is best practice to coordinate and discuss customization plans with the wider Arches open source community. If you haven't already done so, please join the `Arches Community Forum <https://community.archesproject.org/>`_!



Customized Applications
=======================
While the Arches extensions architecture offers a great deal of flexibility (see below), there may be scenarios where you need additional flexibility. From a sustainability and maintenance perspective, this scenario has important risks that need to be understood and factored into long term resource planning and engineering.

Managing long term sustainability and maintenance risks should be a core software engineering focus. As much as possible, you should ideally isolate your customized module as much as possible from the core of Arches. One way preferred way to accomplish this is to develop  **Arches Applications** (see: :ref:`Creating Applications`), which are discrete Python packages that can be integrated into one or more Arches projects. The **Arches Applications** documentation details their development as well as their sustainability advantages.

Arches Applications are a powerful way to create customizations that are isolated from the core of Arches. This isolation can help to reduce the risk of future maintenance and upgrade challenges. Arches Applications can be developed and maintained independently of the core Arches software, and can be shared with the wider Arches community. This can help to ensure that your customizations are more maintainable over time. Arches Applications can also be used to create reusable components that can be shared with members of the Arches community, which can help to reduce the overall cost of development and maintenance.



Custom Extensions
==================================
To increase the likelihood that customizations will have long term compatibility and maintainability with Arches, please use the customization patterns supported and documented by Arches. These patterns include:


- **Extensions** (see: :ref:`Creating Extensions`)
    - card components
    - datatypes
    - functions
    - plugins
    - reports
    - search filters
    - widgets
    - workflows
- **New map layers** (see: :ref:`Creating New Map Layers`)
- **HTML export templates** (see: :ref:`Creating HTML Export Templates`)

Adherence to the extension design patterns helps to isolate your customizations from changes to the core of Arches. Following Arches extensions design patterns will also increase the likelihood that there will be relevant documentation and community help if the extensions need updates in the future. Certain customizations are easier to maintain over time. For example, an overwritten HTML template is generally simpler to upgrade than an inherited Arches Python class or an overwritten Django view. You should factor such considerations into long term resource planning.


API Based Customizations
========================
The Arches :ref:`API` can be used to support customizations, especially those involving integration of Arches with other information systems. Channeling all connections between Arches and other systems through the API aligns with a design practice often described as "`Loose Coupling <https://en.wikipedia.org/wiki/Loose_coupling>`_". By carefully limiting and simplifying how core Arches interfaces with external information systems, you reduce future maintenance burdens, because problems can be identified and fixed in a more focused manner.


Strive for Graceful Degradation
===============================
Things break over time, especially if they are customized and not widely supported by broader community. One way to help manage long term risks is to plan for "graceful degradation". If your custom module is isolated from core Arches (via **Arches App** development and/or loose coupling of API integrations), then if it breaks or can no longer be maintained, the core Arches system should still be perfectly serviceable. Planning for obsolescence and the retirement of hard-to-maintain components is often essential in contexts where Arches is deployed, especially in the cultural heritage sector.
