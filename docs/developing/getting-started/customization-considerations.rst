###################################
Arches Customization Considerations
###################################

If you are leading a project or organization considering customizing Arches software, please read this document carefully. Customization is an inherently risky endeavor, especially if you need to maintain and support your information systems over multiple years.

The practices described here will reduce costs, reduce long term maintenance and security risks, and will lead to greater impact, enhanced sustainability, and open doors for future opportunities. That said, to maximize sustainability, security, maintainability, quality and impact, it is best practice to coordinate and discuss customization plans with the wider Arches open source community. If you haven't already done so, please join the `Arches Community Forum <https://community.archesproject.org/>`_!


More Sustainable Pathways toward Customization
==============================================
To increase the likelihood that customizations will have long term compatibility and maintainability with Arches, please follow the suggested patterns for developing Arches Extensions (see: :ref:`Creating Extensions`). Adherence to the extension design patterns helps to isolate your customizations from changes to the core of Arches. Following Arches extensions design patterns will also increase the likelihood that there will be relevant documentation and community help if the extensions need updates in the future.


Customizations Beyond Extensions
================================
While the Arches extensions architecture offers a great deal of flexibility, there may be scenarios where you need additional flexibility. From a sustainability and maintenance perspective, this scenario has important risks that need to be understood and factored into long term resource planning and engineering.

Managing long term sustainability and maintenance risks should be a core software engineering focus. As much as possible, you should ideally isolate your customized module as much as possible from the core of Arches. One way preferred way to accomplish this is to develop  **Arches Apps** (see: :ref:`Creating Applications`), which are discrete Python packages that can be integrated into one or more Arches projects. The **Arches Apps** documentation details their sustainability advantages.


API Based Customizations
========================
The Arches :ref:`API` can be used to support customizations, especially those involving integration of Arches with other information systems. Channeling all connections between Arches and other systems through the API aligns with a design practice often described as "`Loose Coupling <https://en.wikipedia.org/wiki/Loose_coupling>`_". By carefully limiting and simplifying how core Arches interfaces with external information systems, you reduce future maintenance burdens, because problems can be identified and fixed in a more focused manner.


Strive for Graceful Degradation
===============================
Things break over time, especially if they are customized and not widely supported by broader community. One way to help manage long term risks is to plan for "graceful degradation". If your custom module is isolated from core Arches (via **Arches App** development and/or loose coupling of API integrations), then if it breaks or can no longer be maintained, the core Arches system should still be perfectly serviceable. Planning for obsolescence and the retirement of hard-to-maintain components is often essential in contexts where Arches is deployed, especially in the cultural heritage sector.
