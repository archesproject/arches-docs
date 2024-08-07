###############
Securing Arches
###############

Organizations also need to consider information security risks and requirements into planning, deployment stategies, data modeling, operations, and maintenance. Doing so will help ensure the integrity and appropriate use of Arches managed data.


Security and Risk Management
============================

Information security needs vary widely. Legal requirements, organization policies, funder requirements, understandings of ethics, operational needs, and the subject matters and topics of datasets can all play a role in shaping data security needs. In some organizational settings, especially in the public sector, data security will require complex technical and operational controls.

In certain contexts, data security risks can involve legal, financial, reputational, harms to your own organization and staff, as well as harms to stakeholding communities. It is important to understand and mitigate these risks. The first step in securing your Arches implementation requires review and assessment of your position within this complex and varied environment. Some Arches implementations will require much more robust protections than required by other implementations. If data management needs require greater levels protection, then you will need additional resources and planning to obtain the additional time, expertise, and financing required to assess and reduce data security vulnerabilities.


General Good Security Practices
===============================

* Avoid collecting sensitive data unless required. One of the most effective strategies to reduce data security risks is to limit and avoid the collection of sensitive information. Limiting collection of sensitive data that is not required by your operational needs reduces your risk exposure. 

* Work in collaboration with stakeholders to develop and implement risk reduction strategies. Understanding information security needs and risks may not be straightforward. Different stakeholders can have specialized knowlwdge and expertise to help inform this understanding. Similarly, consultation with different cultural communities can help broaden the cultural and historical perspectives necessary to understand data sensitivities and risks. Building collaborations across communities helps to better inform your information security strategies. It also helps to build trust and good will-- all key to limiting harms in the event of possible data breeches. 

* Use strong passwords. A strong password is a combination of characters that resists easy access by trial and error guesswork. One of the most basic, and easiest to implement security measures on can use to protect an Arche instance from unauthorized access. Strong passwords should be used for Arches administrative ("super-user") accounts and connections to Arches dependencies, especially the PostgreSQL database server.

* Use HTTPS on the Web. Use of HTTPS is a critical aspect of securing your Arches instance. If you do not use HTTPS, passwords and other credentials are visible and can be intercepted. 

* Turn off ``DEBUG`` mode. While testing and developing your Arches instance, it is very helpful to run Arches with the ``DEBUG = True`` setting. That setting provides important debugging information to diagnose and fix problems. However, the ``DEBUG = True`` setting should absolutely **NOT** be used in production, because the diagnostic information provided by debug mode can contain sensitive data. In production contexts, be sure to use the ``DEBUG = False`` setting.



Securing the Deployment Environment
===================================




