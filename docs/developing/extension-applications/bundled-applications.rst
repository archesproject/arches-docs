################################
Applications Bundled with Arches
################################

As of Arches 8.2.0, three Arches extension applications ship inside the ``arches``
distribution itself rather than as separately released packages:

.. list-table::
    :header-rows: 1
    :widths: 30 35 35

    * - Application
      - Module path
      - App label
    * - Arches Querysets
      - ``arches.extensions.querysets``
      - ``arches_querysets``
    * - Arches Vue Components
      - ``arches.extensions.vue_components``
      - ``arches_vue_components``
    * - Arches Controlled Lists
      - ``arches.extensions.controlled_lists``
      - ``arches_controlled_lists``

Because they ship with Arches, there is nothing to ``pip install`` and nothing to add to
your project's ``pyproject.toml``. They are versioned and released with Arches, so their
compatibility with any given Arches release is guaranteed by construction.

They remain optional. Each is enabled by adding it to ``INSTALLED_APPS``, and a project
that enables none of them behaves exactly as it did before.

.. note::
    A project generated with ``arches-admin startproject`` on Arches 8.2.0 or later
    already has everything described on this page. These instructions are for adding the
    applications to a project created on an earlier version.


Module Paths
============

The move changed each application's Python module path, but **not** its app label. The
label is what names the database tables, the migration history, the URL namespace and the
frontend path alias, so none of those change and there is no data migration to run.

.. list-table::
    :header-rows: 1
    :widths: 50 50

    * - Before 8.2.0
      - 8.2.0 and later
    * - ``arches_querysets``
      - ``arches.extensions.querysets``
    * - ``arches_vue_components``
      - ``arches.extensions.vue_components``
    * - ``arches_controlled_lists``
      - ``arches.extensions.controlled_lists``

Both spellings work in 8.2.0. A compatibility alias resolves the old top-level paths —
in Python imports and in the dotted paths Django reads out of settings, such as
``INSTALLED_APPS``, ``ELASTICSEARCH_CUSTOM_INDEXES`` and ``ES_MAPPING_MODIFIER_CLASSES`` —
while raising a ``DeprecationWarning``. The system check ``arches.W002`` flags any
``INSTALLED_APPS`` entry still using an old path.

.. warning::
    The compatibility alias is scheduled for removal in Arches 9.0. Update your imports
    and settings to the new module paths before then.


Migrating from Separately Installed Packages
============================================

If you were already running any of these as pip-installed packages, uninstall them and
remove them from your project's ``pyproject.toml`` first, so that the copies bundled with
Arches are the ones that load:

.. code-block:: bash

    pip uninstall arches-querysets arches-vue-components arches-controlled-lists

Their app labels, database tables and migration history are unchanged by the move, so
there is no data migration to run and no reindexing required. Your existing settings and
imports keep working through the compatibility alias; update them to the new module paths
at your convenience.

Otherwise, the rest of this page is the same as a first-time setup.


Enabling the Applications
=========================

Skip any application you do not want, along with the settings that reference it.

INSTALLED_APPS
--------------

Add the applications to ``INSTALLED_APPS`` in your project's ``settings.py``. They must
be listed after your own project app and before ``"arches"``:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        "django.contrib.postgres",  # required by controlled_lists, whose ListItem uses ExclusionConstraint
        "rest_framework",           # required by the querysets REST layer
        ...
        "<project_name>",
        "arches.extensions.querysets",
        "arches.extensions.vue_components",
        "arches.extensions.controlled_lists",
    )

Two ordering rules apply:

* The bundled applications must precede ``"arches"``. Django resolves management commands
  by walking ``INSTALLED_APPS`` in reverse, so an application listed earlier wins, and
  ``arches_vue_components`` ships its own ``validate`` command that overrides the core one.
* ``controlled_lists`` must follow ``querysets``. It registers a serializer against
  querysets in its ``AppConfig.ready()``.

Two supporting Django applications are also required:

* ``django.contrib.postgres`` — needed only by ``controlled_lists``, whose ``ListItem``
  model uses ``ExclusionConstraint``.
* ``rest_framework`` — needed by the ``querysets`` REST layer. ``djangorestframework`` is
  a core Arches dependency as of 8.2.0, so it is already installed.

Caches
------

``arches.settings`` sets two cache aliases used by ``querysets``:

.. code-block:: python

    ARCHES_QUERYSETS_CONCEPT_CACHE = "querysets_concepts"
    ARCHES_QUERYSETS_RESOURCE_INSTANCE_CACHE = "querysets_resource_instances"

Both must name entries in ``CACHES``. Most projects redefine ``CACHES`` wholesale after
star-importing ``arches.settings``, which drops the inherited entries, so add them back:

.. code-block:: python

    CACHES = {
        ...
        'querysets_concepts': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'querysets_concepts_cache',
            'TIMEOUT': 86400,  # one day in seconds
            'OPTIONS': {'MAX_ENTRIES': 1000},
        },
        'querysets_resource_instances': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'querysets_resource_instances_cache',
            'TIMEOUT': 86400,  # one day in seconds
            'OPTIONS': {'MAX_ENTRIES': 1000},
        },
    }

If an alias names a cache that does not exist, the system check ``arches_querysets.E001``
fails at startup. Setting either alias to ``None`` falls back to the default cache and
raises the warning ``arches_querysets.W001`` instead.

Reference Index
---------------

``controlled_lists`` stores its reference data in a dedicated Elasticsearch index. Arches
provides the index name as ``REFERENCES_INDEX_NAME`` but deliberately leaves the index
itself project-declared, so that projects which do not enable the application are not made
to build it.

.. code-block:: python

    ELASTICSEARCH_CUSTOM_INDEXES = [
        {
            'module': 'arches.extensions.controlled_lists.search_indexes.reference_index.ReferenceIndex',
            'name': REFERENCES_INDEX_NAME,
            'should_update_asynchronously': True,
        },
    ]

    # Makes reference data searchable from the term search bar.
    TERM_SEARCH_TYPES = list(TERM_SEARCH_TYPES) + [
        {
            'type': 'reference',
            'label': _('References'),
            'key': REFERENCES_INDEX_NAME,
            'module': 'arches.extensions.controlled_lists.search_indexes.reference_index.ReferenceIndex',
        },
    ]

    # Indexes reference values alongside the resources that use them.
    ES_MAPPING_MODIFIER_CLASSES = [
        "arches.extensions.controlled_lists.search.references_es_mapping_modifier.ReferencesEsMappingModifier",
    ]

URLs
----

Mount the applications' routes in your project's ``urls.py``, ahead of the core Arches
routes:

.. code-block:: python

    urlpatterns.append(path('', include('arches.extensions.querysets.urls')))
    urlpatterns.append(path('', include('arches.extensions.vue_components.urls')))
    urlpatterns.append(path('', include('arches.extensions.controlled_lists.urls')))

.. note::
    If your project uses ``django_hosts``, make sure your ``hosts.py`` points at your
    project's own ``urls.py``. ``django_hosts`` sets ``request.urlconf`` from the matched
    host, so requests resolve against whatever urlconf the host names — even when
    ``reverse()`` returns correct paths from ``ROOT_URLCONF``.

Migrate and Build
-----------------

Run migrations, create the reference index, and rebuild the frontend:

.. code-block:: bash

    python manage.py migrate
    python manage.py es setup_indexes -n references
    npm install
    npm run build_development

``es setup_indexes`` creates the index; on a first-time setup there is no reference data
to index yet. If you are enabling ``controlled_lists`` on a project that already holds
reference data, populate the index as well:

.. code-block:: bash

    python manage.py es index_database -n references


Datatype Overrides
==================

``arches.extensions.querysets`` ships its own implementations of several core datatypes.
Arches resolves datatypes from installed applications before core, so enabling the
application overrides core's ``file-list``, ``concept``, ``concept-list``,
``resource-instance``, ``resource-instance-list``, ``node-value``, ``string``, ``url`` and
``geojson-feature-collection`` datatypes throughout the application, not only in the
querysets ORM layer.

This is the same mechanism any Arches extension application uses to extend a datatype, and
it applied equally when ``arches-querysets`` was installed as a separate package. It is
called out here because projects generated on 8.2.0 enable the application by default.
Projects upgrading from an earlier version keep core's datatypes until they add
``arches.extensions.querysets`` to ``INSTALLED_APPS``.
