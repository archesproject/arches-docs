#################
Localizing Arches
#################

If you want to support localization in your Arches instance, you'll first need to install `gettext <https://www.gnu.org/software/gettext/>`_ on your system. This tool provides the basis for multilingual support for your Arches instance.

.. code-block:: bash

    apt update
    apt upgrade
    apt install gettext libgettextpo-dev

After `gettext` is installed, continue with the following steps:

1. Update your settings.py (or settings_local.py) file by adding this import statement at the top:

.. code-block:: python

    from django.utils.translation import gettext_lazy as _

2. Next copy the MIDDLEWARE setting to your project's settings.py file.  If it's already in your settings.py file, be sure to uncomment ```"django.middleware.locale.LocaleMiddleware"```

.. code-block:: python

    MIDDLEWARE = [
        # 'debug_toolbar.middleware.DebugToolbarMiddleware',
        "corsheaders.middleware.CorsMiddleware",
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        #'arches.app.utils.middleware.TokenMiddleware',
        "django.middleware.locale.LocaleMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "arches.app.utils.middleware.ModifyAuthorizationHeader",
        "oauth2_provider.middleware.OAuth2TokenMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        # "django.middleware.clickjacking.XFrameOptionsMiddleware",
        "arches.app.utils.middleware.SetAnonymousUser",
    ]

3. Next add the LANGUAGE_CODE, LANGUAGES, and SHOW_LANGUAGE_SWITCH to your project's settings.py file and update them to reflect your project's requirements:

.. code-block:: python

    # default language of the application
    # language code needs to be all lower case with the form:
    # {langcode}-{regioncode} eg: en, en-gb ....
    # a list of language codes can be found here http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = "en"
    # list of languages to display in the language switcher, 
    # if left empty or with a single entry then the switch won't be displayed
    # language codes need to be all lower case with the form:
    # {langcode}-{regioncode} eg: en, en-gb ....
    # a list of language codes can be found here http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGES = [
        ('de', _('German')),
        ('en', _('English')),
        ('en-gb', _('British English')),
        ('es', _('Spanish')),
    ]
    # override this to permenantly display/hide the language switcher
    SHOW_LANGUAGE_SWITCH = len(LANGUAGES) > 1

4. Now add this import statement to the top of your urls.py file:

.. code-block:: python

    from django.conf.urls.i18n import i18n_patterns
    
5. Finally add the following code to the end of your urls.py file:

.. code-block:: python

    if settings.SHOW_LANGUAGE_SWITCH is True:
        urlpatterns = i18n_patterns(*urlpatterns)

----

Once the system is prepared for localization, the next steps involve generating a Django message file or .po file which will contain all available translation strings in Arches and how they should be translated in any given language.

For more information, see `Localization: how to create language files <https://docs.djangoproject.com/en/stable/topics/i18n/translation/#localization-how-to-create-language-files>`_ in the Django documentation.

There are some example commands to make and load PO files in the core arches settings file that can be found `here <https://github.com/archesproject/arches/blob/dev/7.0.x/arches/settings.py#L193>`_. If loading a new PO file, simply replace the existing po file and run compilemessages.

**************************************
Localizing Graph Strings within Arches
**************************************

You can also export strings from your custom Arches templates for localization using the following Django admin commands (in these examples, we are using the French language code "fr"). 

1. The first Django-Admin command is:

    .. code-block:: bash

        python django-admin makemessages -l fr 
    

    If for some reason you're using language code fr-fr or another regionalized language code, capitalize the second pair of letters, ie, fr-FR or en-GB. In any case, ignore any messages about skipped files due to invalid start bytes, this is normal.

2. The second Django-Admin command is:

    .. code-block:: bash

        python django-admin compilemessages


    You may get a ton of error messages reading something like: `Execution of msgfmt failed: $filename 'msgid' and 'msgstr' entries do not both begin with '\n'.` Just ignore this and run the compilemessages command again until it works.


Arches also supplies a command to generate PO files to localize graphs you have created in your Arches instance:

.. code-block:: bash

    # This command will create a graph.po file in the locale directory for each language specified in the LANGUAGES array in settings.py
    python manage.py i18n makemessages


The standardized PO (``.po``) files generated by the commands above can be edited (potentially in collaboration and under version control). After you develop the `.po` file, you can import it with the following command:

.. code-block:: bash

    python manage.py i18n loadmessages

This will attempt to load the graph translation files (graph.po files) for every language specified in the ``LANGUAGES`` array from settings.py.




*******************************
Localizing the Arches Front End
*******************************

If you make changes to language configuration settings in Arches, you will need to rebuild the Arches front end to reflect those changes. To do so, navigate to your Arches project directory and run the following command:

.. code-block:: bash

    # remove any node_modules that might have been installed by the arches install
    rm -rf node_modules
    rm -f package-lock.json
    # Now do the NPM install
    npm install
    npm run build_development
    # Now collect the static files again
    python manage.py collectstatic --clear --noinput



************************************************
Setting up Localized Languages for Business Data
************************************************

By default, every language from the LANGUAGES array in settings.py is available for business data entry.
To add additional languages for business data entry only, you can do the following. 

1.  Access the admin page (``http://localhost:8000/admin/``)
2.  Choose the "Languages" table.  (``http://localhost:8000/models/language``)
3.  Select "Add Language"
4.  Fill in information on new language, including a default direction.

Repeat this process for all new languages you wish to add. 

Additionally, remove any languages you do not plan on using.  

Once this is complete, text widgets should be able to write data in the desired languages.

***********************
RDF Imports and Exports
***********************

Business data can be exported in RDF format. The directionality of the string data will be lost as 
the RDF specification does not include directionality. There is an 
`active attempt <https://w3c.github.io/rdf-dir-literal/>`_ to include direction within the 
RDF specification.

***********************
CSV Exports and Imports
***********************

It is possible to import and export localized business data through CSV format. There is a ``--language``
switch that will limit the languages that will be exported (all languages are exported by default). 
However, if attempting to re-import a limited subset of languages through the csv importer, entire 
string objects will be overwritten by the subset. For example, if a string node has values for 
English, Spanish, and French, the subset of languages can be limited by specifying

.. code-block:: bash

    --languages en,es

If attempting to import the resulting csv, any values that were pre-existing for French would be 
overwritten in "overwrite" mode or added as a separate tile in "append" mode. There is currently
no way to merge these values. If the intention is to re-import the csv values later, export all
languages.
