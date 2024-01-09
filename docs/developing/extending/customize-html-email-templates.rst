################################
Customizing HTML Email Templates
################################

In addition to the standard email templates that are provided by Arches, from version 7.5 is possible to customize ("customise", if not spelled in the US) HTML email templates in your Arches project to include such things as branding, logos, custom text and other elements specific to a given instance.

A developer will need to customize the starting templates and add any extra context items to the settings file which are required by the templates.



Templates and their Locations
=============================

Main Templates
--------------

The starting templates provided when you create a new project are:

- Download Read Email Notification
- General Notification
- Package Load Completion Notification

These templates are located in the following directory:
`<project name>/templates/emails/`

They overwrite the out-of-the-box templates found in the arches install directory.  If you do not wish the arches install directory versions to be overwritten then remove these templates from the project directory.

They consist of static text and variables.  The variables are used to render the email with the appropriate context items.  The variables are enclosed in double curly braces, e.g. {{ variable_name }}.


Templates for Common Styling and Formatting
-------------------------------------------

There are also three files supplied which are referenced in the above templates as includes.  These files allow for common styling and formatting to be applied to all the HTML email templates.  These files are:
- custom_email_css.htm
- custom_email_footer.htm
- custom_email_header.htm

Initially the above files are empty.

The files are located in the following directory:
`<project name>/templates`

When adding an image logo, you may wish to do so in Base64 encoded format to ensure the images appear as expected in the email.  There are a number of online tools that can be used to convert an image to Base64 format.



Extra Context Items
===================

In some instances, you may wish to add extra context items which are used by the template to render the email.  These context items are stored in the ``EXTRA_EMAIL_CONTEXT`` setting within the settings.py or settings_local.py file.

The starting default ``EXTRA_EMAIL_CONTEXT`` object contains the value for Salutation and a expiration date that is based on the ``CELERY_SEARCH_EXPORT_EXPIRES`` setting.

For the sake of consistency, if you are using common templated text across templates while not in the default context items, it is recommended that you add it to the ``EXTRA_EMAIL_CONTEXT`` setting.

For example, if you have a common email address that you wish to use across all templates, you could add it to the ``EXTRA_EMAIL_CONTEXT`` setting as follows:

.. code-block:: python

        EXTRA_EMAIL_CONTEXT = {
                "salutation": ("Hi"),
                "expiration":(
                        datetime.now()
                        + timedelta(seconds=CELERY_SEARCH_EXPORT_EXPIRES)
                ).strftime("%A, %d %B %Y"),
                "email_address": ("person@example.org"),
        }

You would then be able to use the tag ``{{ email_address }}`` to render the email address in your template(s).


Other Considerations
====================

You are advised, when creating customized HTML email templates, to ensure the templates are accessible.  For further information on configuring your templates to be accessible, see the :ref:`Accessibility` section.
