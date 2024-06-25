########################
Settings - Beyond the UI
########################

In reality, many more settings are used than are exposed in the UI. To see **all settings** look in the `core Arches settings.py file <https://github.com/archesproject/arches/blob/master/arches/settings.py>`_ (we try to leave comments on each one). The way these settings are cascaded through the app, and where they can be overwritten as needed, is described below.

Settings Inheritance
--------------------

Settings can be defined in many different places. Here is the full inheritance pattern for a typical Arches project:

- ``arches/settings.py``
    If you installed Arches through pypi (``pip install arches``) this file will be deep in your virtual environment, and you shouldn't touch it.

    ↓  `values here can be superceded by...`  ↓

- ``my_project/my_project/settings.py``
    Settings here define backend information specific to your app. For example, this is where you would add new references to template context processors.

    ↓  `values here can be superceded by...`  ↓

- ``my_project/my_project/package_settings.py`` (optional)
    Settings here define backend information specific to the package loaded to your app. You do not need to create or modify this file as it will be loaded when you load a package. However, you may want to edit this file if your intent is to design or modify a package.

    ↓  `values here can be superceded by...`  ↓

- ``my_project/my_project/settings_local.py`` (optional)
    Typically kept out of version control, a settings_local.py file is used for 1) sensitive information like db credentials or keys and 2) environment-specific settings, like paths needed for production configuration.

    ↓  `values here can be superceded by...`  ↓

- System Settings Manager
    Settings exposed to the UI are the end of the inheritance chain. In fact, these settings are stored as a resource in the database, and the contents of this resource is defined in the System Settings Graph. Nodes in this graph with a name that matches a previously defined setting (i.e. in the files above) will override that value with whatever has been entered through the UI.

----

If you're a developer, you'll notice that the codebase uses::

    from arches.app.models.system_settings import settings

in favor of::

    from django.conf import settings

This is to ensure that UI settings are implemented properly. If you are using settings outside of a UI context you will need to follow the import statement with ``settings.update_from_db()``.

Password Validators
-------------------

By default, Arches requires that passwords meet the following criteria:

- Have at least one numeric and one alphabetic character
- Contain at least one special character
- Have a minimum length of 9 characters
- Have at least one upper and one lower case character

Admins can change these requirements by configuring the `AUTH_PASSWORD_VALIDATORS`:code: setting in their projects **settings_local.py** file. Below is the default validator setting:

.. code-block:: python

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'arches.app.utils.password_validation.NumericPasswordValidator', #Passwords cannot be entirely numeric
        },
        {
            'NAME': 'arches.app.utils.password_validation.SpecialCharacterValidator', #Passwords must contain special characters
            'OPTIONS': {
                'special_characters': ('!','@','#',')','(','*','&','^','%','$'),
            }
        },
        {
            'NAME': 'arches.app.utils.password_validation.HasNumericCharacterValidator', #Passwords must contain 1 or more numbers
        },
        {
            'NAME': 'arches.app.utils.password_validation.HasUpperAndLowerCaseValidator', #Passwords must contain upper and lower characters
        },
        {
            'NAME': 'arches.app.utils.password_validation.MinLengthValidator', #Passwords must meet minimum length requirement
            'OPTIONS': {
                'min_length': 9,
            }
        },
    ]

To **remove a password validator** in Arches, you can simply remove a validator from the list of `AUTH_PASSWORD_VALIDATORS`:code:.

To modify the list of **required special characters**, simply edit the list of characters in the `special_characters`:code: option in the `SpecialCharacterValidator` validator.

To change the **minimum length of a password**, change the `min_length`:code: property in the `MinLengthValidator`:code: validator.

Advanced users can override or add new validators by creating their own validation classes as explained in `Django's password validation documentation <https://docs.djangoproject.com/en/stable/topics/auth/passwords/#module-django.contrib.auth.password_validation/>`_.

Time Wheel Configuration
------------------------

By default Arches will bin your data in the search page time wheel based on your data's temporal distribution. This enables Arches to bin your data efficiently. If your data spans over 1000 years, the bins will be by millennium, half-millennium and century. If your data spans less than a thousand years, your data will be binned by millennium, century, and decade.

You may decide, however, that the bins do not reflect your data very well, and in that case you can manually define your time wheel configuration by editing the TIMEWHEEL_DATE_TIERS setting.

Here is an example of a custom time wheel::

    TIMEWHEEL_DATE_TIERS = {
    "name": "Millennium",
    "interval": 1000,
    "root": True,
    "child": {
            "name": "Century",
            "interval": 100,
            "range": {"min": 1500, "max": 2000},
            "child": {
                "name": "Decade",
                "interval": 10,
                "range": {"min": 1750, "max": 2000}
            }
        }
    }

Each tier, ('Millennium', 'Century', 'Decade' are each tiers) will be reflected as ring in the time wheel.
Properties:

    - "name" - The name that will appear in the description of the selected period
    - "interval" - The number of years in each bin. For example, if your data spans 3000 years, and your interval is 1000, you will get three bins in that tier.
    - "root" - This applies only to the root of the config and should not be modified.
    - "child" - Adding a child will add an additional tier to your time wheel. You can nest as deeply as you like, but the higher the resolution of your time wheel, the longer it will take to generate the wheel.
    - "range" - A range is optional, but including one will restrict the bins to only those within the range.

If you do need to represent decades or years in your time wheel and this impacts performance, you can cache the time wheel for users that may load the search page frequently. To do so, you just need to activate caching for your project.
If you have Memcached running at the following location `127.0.0.1:11211` then the time wheel will automatically be cached for the 'anonymous' user. If not you can update the CACHES setting of your project::

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': os.path.join(APP_ROOT, 'tmp', 'djangocache'),
            'OPTIONS': {
                'MAX_ENTRIES': 1000
            }
        }
    }

This will cache the time wheel to your project's directory. There are other ways to define your cache that you may want to use. You can read more about those options in `Django's cache documentation <https://docs.djangoproject.com/en/stable/topics/cache/>`_.

By default the time wheel will only be cached for 'anonymous' user for 24 hours. To add other users or to change the cache duration, you will need to modify this setting::

    `CACHE_BY_USER = {'anonymous': 3600  * 24}`

The CACHE_BY_USER keys are user names and their corresponding value is the duration (in seconds) of the cache for that user.
For example, if I wanted to cache the time wheel for the admin user for 5 minutes, I would change the CACHE_BY_USER setting to::

    `CACHE_BY_USER = {'anonymous': 3600  * 24, 'admin': 300}`


Configuring Captcha
-------------------

Setting up your captcha will help protect your production from spam and other unwanted bots. To set up your production with captcha, first `register your captcha <https://www.google.com/recaptcha/intro/v3beta.html>`_ and then add the captcha keys to your project's settings.py. Do this by adding the following::

    RECAPTCHA_PUBLIC_KEY = 'x'
    RECAPTCHA_PRIVATE_KEY = 'x'

Replace the x's with your captcha keys.

Enabling User Sign-up
---------------------

To enable users to sign up through the Arches UI, you will have to add the following lines of code to your project's settings.py::

    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'xxxx@xxx.com'
    EMAIL_HOST_PASSWORD = 'xxxxxxx'
    EMAIL_PORT = 587

Update the EMAIL_HOST_USER and EMAIL_HOST_PASSWORD with the correct email credentials and save the file. It is possible that this may not be enough to support your production of Arches. In that case, there's more information on setting up an email backend on the `Django site <https://docs.djangoproject.com/en/stable/topics/email/#smtp-backend>`_.

To configure what group new users are put into, add the following lines of code to your project's settings.py::

    # group to assign users who self sign up via the web ui
    USER_SIGNUP_GROUP = 'Crowdsource Editor'

If you would like to change which group new users are added to, replace 'Crowdsource Editor' with the group you would like to use.

Using Single Sign-On With an External OAuth Provider
----------------------------------------------------

To take advantage of single sign-on using an organiztion's identity provider, users can be routed through an external OAuth provider for authentication based on their email's domain.

Your arches application will need to use SSL and be configured with an application ID from your provider.  This application ID will need to be configured with a redirect URL to your Arches application at auth/eoauth_cb, for example: https://qa.archesproject.org/auth/eoauth_cb

Once your application is set up with the provider, you can configure Arches to use it by updating EXTERNAL_OAUTH_CONFIGURATION, for example using an Azure AD tenant could look something like this:

.. code-block:: python

    EXTERNAL_OAUTH_CONFIGURATION = {
        # these groups will be assigned to OAuth authenticated users on their first login
        "default_user_groups": ["Resource Editor"],
        # users who enter an email address with one of these domains will be authenticated through external OAuth
        "user_domains": ["archesproject.org"],
        # claim to be used to assign arches username from
        "uid_claim": "preferred_username",
        # application ID and secret assigned to your arches application
        "app_id": "my_app_id",
        "app_secret": "my_app_secret",
        # provider scopes must at least give Arches access to openid, email and profile
        "scopes": ["User.Read", "email", "profile", "openid", "offline_access"],
        # authorization, token and jwks URIs must be configured for your provider
        "authorization_endpoint": "https://login.microsoftonline.com/my_tenant_id/oauth2/v2.0/authorize",
        "token_endpoint": "https://login.microsoftonline.com/my_tenant_id/oauth2/v2.0/token",
        "jwks_uri": "https://login.microsoftonline.com/my_tenant_id/discovery/v2.0/keys"
        # enforces token validation on authentication, AVOID setting this to False
        "validate_id_token": True,
    }


Accessibility Mode
------------------
As of version 7.5, Arches can be configured to meet `WCAG <https://www.w3.org/WAI/standards-guidelines/wcag/>`_ defined **AA** level accessibility requirements for all public facing user interfaces (all content available to anonymous users without a login, including the home page, search interface, and resource reports). Improved accessibility helps to promote a more welcoming and inclusive community, and may help to meet important legal and ethical requirements, especially for institutions that serve the public.

To enable the "Accessibility Mode", update your Arches project **settings.py** or **settings_local.py** file and add:

.. code-block:: python

    # Activate accessibility mode
    ACCESSIBILITY_MODE = True


Once you've saved that change, restart Arches. Arches should now display more accessible user interfaces for public facing content. The specific accessibility enhancements activated in Accessibility Mode include:

- Markup to support labeling for screen readers
- Tabbing to support natural flow through the site
- Improved focus management especially when interacting with popup/slide out panels
- Updated drop downs to use an accessible version
- Updated text contrast
- Updated html to reflow properly on smaller screen sizes or when the screen is zoomed up to 400%
- Updated text sizes to use relative sizing

File type checking
------------------
Through the `FILE_TYPE_CHECKING` setting, Arches provides three modes for file type checking:

- `None`: files can be uploaded regardless of the `FILE_TYPES` setting. In addition, the integrity checks described below for .csv, .zip, .xlsx, and .json files are skipped.
- `"lenient"`: if the type of the uploaded file can be guessed, the following checks are performed:
    - The guessed file type must be included in `FILE_TYPES`
    - Each row of a .csv file must have the same length as the header (not jagged)
    - An .xlsx file must be a valid excel workbook
    - .csv and .json files must be parsable
    - Files inside a .zip archive will be tested against all of the above
- `"strict"`: In addition to the above checks, files for which a type cannot be detected are rejected.

When evaluating your file type checking security posture, keep in mind that `"strict"` mode will prevent uploading of simple `.txt` files, as there is no well-known type for them.

.. versionadded:: 7.6
    The `"lenient"` option.

.. versionchanged:: 7.6
    Boolean values are deprecated. Until version 8, `True` maps to `"strict"`,
    and `False` maps to `None`. In version 8, providing boolean values will
    raise an exception.

.. note::
    Some files that look like artifacts from creating .zip archives on Macs,
    such as files beginning with "__MACOSX" or ending with "DS_Store" are
    currently permitted when contained in .zip archives, even in strict mode,
    but this behavior may change in future versions of Arches.
