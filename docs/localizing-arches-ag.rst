#################
Localization
#################

*****************************************************
Setting up Localized Languages for the User Interface
*****************************************************

There are two places to set language codes within arches.  First, setttings.py contains languages specific to
the Arches UI.  


.. code-block:: python

    LANGUAGES = [
        ("de", _("German")),
        ("en", _("English")),
        ("en-gb", _("British English")),
        ("en-us", _("US English"))
    ]

Also set the LANGUAGE_CODE to be the default language code of your arches install.  

.. code-block:: python

    LANGUAGE_CODE = "en"

Then, import the localized strings for the languages that will be used. 

.. code-block:: bash

    manage.py i18n loadmessages

This will attempt to load the translation files (po files) for every language specified
in the LANGUAGES array from settings.py.


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

**************************************
Creating PO Files for New Translations
**************************************

To export Arches User Interface strings for translation into new languages, first make sure that
the new language has been added to LANGUAGES in settings.py.  Then, run the following command.  

.. code-block:: bash

    manage.py i18n makemessages

This will generate a new PO file with all of the Arches strings that need to be translated.  

***********************
RDF Imports and Exports
***********************

Business data can be exported in RDF format.  The directionality of the string data will be lost as 
the RDF specification does not include directionality.  There is an 
`active attempt <https://w3c.github.io/rdf-dir-literal/>`_ to include direction within the 
RDF specification.  

***********************
CSV Exports and Imports
***********************

It is possible to import and export localized business data through CSV format.  There is a --language
switch that will limit the languages that will be exported (all languages are exported by default).  
However, if attempting to re-import a limited subset of languages through the csv importer, entire 
string objects will be overwritten by the subset.  For example, if a string node has values for 
English, Spanish, and French, the subset of languages can be limited by specifying

.. code-block:: bash

    --languages en,es

If attempting to import the resulting csv, any values that were pre-existing for French would be 
overwritten in "overwrite" mode or added as a separate tile in "append" mode.  There is currently
no way to merge these values.  If the intention is to re-import the csv values later, export all
languages.  

**********************
Additional Information
**********************

Text widgets default to the current UI language.  
