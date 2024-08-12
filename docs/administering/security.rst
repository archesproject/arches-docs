###############
Securing Arches
###############

Organizations also need to consider information security risks and requirements into planning, deployment stategies, data modeling, operations, and maintenance. Doing so will help ensure the integrity and appropriate use of Arches managed data.


Security and Risk Management
============================

Information security needs vary widely. Legal requirements, organization policies, contract or funder requirements, understandings of ethics, operational needs, and the specifics of the information documented in your data can all play a role in shaping data security needs. In some organizational settings, especially in the public sector, data security will require complex technical and operational controls. Even information intended for public release will require measures to protect against accidental or unauthorized attempts at modification or deletion.

In certain contexts, data security risks can involve legal, financial, reputational, harms to your own organization and staff, as well as harms to stakeholding communities. It is important to understand and mitigate these risks. The first step in securing your Arches implementation requires review and assessment of your position within this complex and varied environment. Some Arches implementations will require much more robust protections than required by other implementations. If data management needs require greater levels protection, then you will need additional resources and planning to obtain the additional time, expertise, and finances required to assess and reduce data security vulnerabilities.


Principle of Least Privilege
============================
The *Principle of Least Privilege* means giving any users account or processes only those privileges required to perform its intended functions, and no more. This approach helps to clarify how to manage security issues. One can implement the *Principle of Least Privilege* using *Default Deny* models to accessing systems. The *Default Deny* cybersecurity model involves denying access by default and allowing only authorized and explicitly permitted activities. In this model, all network communications and software requests are *denied* unless specifically approved or permitted through predefined rules and policies. 

Arches version 7.6 implements a *Default Deny* setting that can be enabled so that Arches administrators need to explicitly determine rules that grant access and modification privileges to Arches managed resource data. Arches version 8 will likely make *Default Deny* the default setting for Arches. The Arches *Default Deny* model only applies to resource data managed within Arches. One still needs to consider other security concerns (networking, protecting Arches servers, human considerations, etc.) as discussed below.


General Good Security Practices
-------------------------------

* **Avoid collecting sensitive data unless required.** One of the most effective strategies to reduce data security risks is to limit and avoid the collection of sensitive information. Limiting collection of sensitive data that is not required by your operational needs reduces your risk exposure. 

* **Work in collaboration with stakeholders** to develop and implement risk reduction strategies. Understanding information security needs and risks may not be straightforward. Different stakeholders can have specialized knowlwdge and expertise to help inform this understanding. Similarly, consultation with different cultural communities can help broaden the cultural and historical perspectives necessary to understand data sensitivities and risks. Building collaborations across communities helps to better inform your information security strategies. It also helps to build trust and good will-- all key to limiting harms in the event of a possible security breach.

* **Encourage good security practices across your team**. People play a fundamental role in good security practices. Develop greater awareness of security needs and practices across your team. Develop processes to handle transitions in roles and responsibilies as the composition of your team changes. Such processes need to answer questions like: "How are passwords and other credentials updated if someone leaves the organization?" Similarly, develop ways to avoid "single point of failure" situations where the unavailability of one person can block access to critical systems.

* **Use strong passwords**. A strong password is a combination of characters that resists easy access by trial and error guesswork. Strong passwords provide one of the easiest to implement security measures one can use to protect an Arches instance from unauthorized access. Strong passwords are especially important for accounts with more privileges. They should be used for all Arches administrative ("super-user") accounts and connections to Arches dependencies, especially the PostgreSQL database server.

* **Enable Multifactor Authentication**. Arches provides optional two-factor authentication features. You can enable these features to provide an additional layer of security by more robustly verifing the identity of users attempting to access the application. (See :ref:`Two-factor Authentication`)

* **Keep your Arches instance up-to-date**. The Arches open-source project sees continual updates and improvements. While some of these updates improve performance and capabilities, many updates also center on improvements to security and fixes to close vulnerabilities. To keep Arches secure, you will need to perform regular updates of your instance. If your organization intends to maintain Arches over long time periods, consider deploying a Long Term Support (LTS) release of Arches. LTS releases will see updates and patch fixes, including security fixes, over longer time periods than other releases. (See :ref:`Arches Releases` and the `Arches Release Roadmap <https://www.archesproject.org/roadmap/>`_)

* **Use HTTPS on the Web**. Use of HTTPS with valid SSL/TSL certificates is a critical aspect of securing your Arches instance because it encrypts and secures communications over the Web. If you do not use HTTPS, passwords and other credentials are visible and can be intercepted. One can use free-of-charge services provided by the nonprofit `Let's Encrypt <https://letsencrypt.org/>`_ to generate and renew valid SSL/TLS certificates. (See more :ref:`Implementing SSL`).

* **Turn off DEBUG mode**. While testing and developing your Arches instance, it is very helpful to run Arches with the ``DEBUG = True`` setting. That setting provides important debugging information to diagnose and fix problems. However, the ``DEBUG = True`` setting should absolutely **NOT** be used in production, because the diagnostic information provided by debug mode can contain sensitive data, sometimes including access credentials. In production contexts, be sure to use the ``DEBUG = False`` setting. (See :ref:`Introduction to Production Deployment`)


Securing the Deployment Environment
-----------------------------------

As discussed, one of the most important aspects of securing an Arches instance centers on protecting the server(s) that host Arches and dependency applications (PostgreSQL, ElasticSearch, etc.). Consider the following measures to improve the security of your Arches hosting servers:

* **Update your Operating System (OS)**. The OS of your Arches server should be regularly updated and patched so keep pace with the latest security improvements and vulnerability fixes.

* **Close ports and limit access to only the intended audience**. In keeping with the *Principle of Least Privilege*, you should block access to all Internet ports on your servers except for those that are needed for Arches to function. Closing ports blocks opportunities for bad actors to access your systems. Similarly, depending on the sensitivity of data in your Arches instance and your operational needs, you can also restrict access to a limited set of known IP addresses. Similarly, one can also restrict network traffic to the PostgreSQL and ElasticSearch servers used by Arches.  

* **Protect your Arches system credentials**. While use of strong passwords is a key security measure, one also needs to protect the server(s) where Arches is deployed. To function, the Arches application needs to be supplied with multiple passwords and other credentials in order to connect with dependency applications, including the PostgreSQL database. These credentials need to be added to or accessible to the ``settings.py`` (or similar ``settings_local.py``) files. To do so, you can choose to store credentials in the ``settings.py`` (or similar) file itself, in seperate configuration files accessed by ``settings.py``, in the system environment variables, or, ideally , in a secret store that helps meet your cybersecurity goals (this being preferred). The credentials represent very sensitive information and need to be secured by protecting the Arches server against unauthorized access. Consider measures to store Arches' system credentials in secure locations off of your server to help prevent accidental disclosure or modification during periods of code updates.

* **Consider encrypted storage**. As an extra security measure, one can encrypt storage systems used by Arches. For example, if Arches is used to manage uploads of digital files (image files, GIS files, external data files, document files, etc.) these files can be mantained in encrypted storage systems. Many popular cloud storage services, including Amazon S3 or Google provide data encyption options. Similarly, Arches managed data stored in stored in a PostgreSQL database or ElasticSearch can also be encrypted.


Expert Help
-----------

Some organizations must manage sensitive data. In these situations, organizations should involve technical experts to secure their Arches deployments. An organization may need to rely on both "in house" expertise (people who manage information systems within an organization) and contracted `Arches service providers <https://www.archesproject.org/service-providers/>`_.


Collaboration to Improve Security
---------------------------------
One of the most important ways strategies to improve Arches security centers on collaboration with the larger Arches open-source community. Some organizations, particularly those in the public sector, have done extensive security audits and penetration testing of Arches. In some cases, they have reported vulnerabilities that were subsequently diagnosed and fixed in the Arches software release process. Reporting vulnerabilities therefore helps improve the security and reliability of Arches for the entire community. Please report any security vulnerability or suspected vulnerability to contact@archesproject.org ! 
