======================================
Arches Search Components Documentation
======================================

What are Search Components?
---------------------------

Arches Search is powered by multiple components, including a search engine from Elasticsearch.
For each search criteria, including geospatial criteria, resource model selections, search terms, etc., there
exists a "Search Component" sometimes called a "Search Filter". These search components give specific instructions to the search engine 
for how to execute the logic of the filter. Developers can either override these search components in their project,
or create new ones to make available to users on their Arches instance. Some level of experience with Elasticsearch is strongly recommended.

To override a search component defined in Core Arches, in your project directory `my_proj/my_proj/search/components/` create a python file of the same name as the search component in Core Arches.
The python logic in this file will be called by Arches when a search component of that name is used.
To create your own search components, you can create the python files in `my_proj/my_proj/search_components/`. More information is available in ../extensions/creating-extensions

Long-term Maintainability
-------------------------

Will your search components break if you upgrade Arches?
If you _override_ core arches extensions, whether search component or card component or other extension types, you will likely need 
to update your overridden version every time you upgrade Arches, even for patch releases.

If you create your own search components in your project, the main things to consider with regard to long-term maintenance 
include:

- the search_components table in the database (whether a new version of Arches introduces data migrations for this table)
- the `arches/app/search/elasticsearch_dsl_builder` classes in core arches: any changes to the Elasticsearch client configuration and its query classes may impact your search component 
- the index mappings at `arches/app/search/mappings.py`: any changes to these indices or their mappings may impact your search component however you can create your own custom index if that makes your customizations more maintainable.


Map Filter
----------

- **Name**: ``MapFilter``
- **Purpose**: Applies spatial filtering to search queries based on user-defined geographic areas and properties.
- **Key Arguments**:
  - ``spatial_filter``: Serialized JSON containing geographic data and attributes to filter search results.
- **Backend Functionality**:
  - Deserializes geographic filter parameters from request.
  - Applies a geometric buffer if specified.
  - Constructs an Elasticsearch query using ``GeoShape`` to filter results within the specified geometry.
  - Supports inverted spatial searches (excludes specified area).
- **Customization**:
  - Extend or modify geometry processing functions to support different spatial analyses.


Term Filter
-----------

- **Name**: ``TermFilter``
- **Purpose**: Applies term-based filtering to search queries, managing both string and concept term filters based on user input.
- **Key Arguments**:
  - ``querysting_params``: Serialized JSON containing terms to filter the search queries, specifying type (term or string) and value.
  - ``language``: Specifies the language context for string-based searches, defaulting to any if not specified.
- **Backend Functionality**:
  - Parses term filters from the request and dynamically constructs nested Elasticsearch queries.
  - Supports phrase matching for term searches and various match strategies for string searches, including prefix and exact match.
  - Handles both standard and provisional data filtering within the specified term context.



Paging Filter
-------------

- **Name**: ``PagingFilter``
- **Purpose**: Manages pagination of search results, handling large datasets by limiting the number of items returned per request.
- **Key Arguments**:
  - ``page``: Current page number.
  - ``limit``: Number of results per page.
- **Backend Functionality**:
  - Determines the appropriate result slice based on page number and limit, adjusting for exports or mobile downloads.
  - Integrates with Elasticsearch pagination features (``start`` and ``limit``).
- **Customization**:
  - Modify the pagination logic to accommodate different types of client-side pagination interfaces.

Provisional Filter
------------------

- **Name**: ``ProvisionalFilter``
- **Purpose**: Filters search results based on the provisional status of resources.
- **Key Arguments**:
  - ``include_provisional``: Flag to include or exclusively search for provisional resources.
- **Backend Functionality**:
  - Applies a filter to include or exclude provisional resources based on the user's choice.


Resource Type Filter
--------------------

- **Name**: ``ResourceTypeFilter``
- **Purpose**: Filters search results based on specified resource types.
- **Key Arguments**:
  - ``resourceTypeFilter``: Serialized JSON defining resource types to filter.
- **Backend Functionality**:
  - Parses resource type identifiers from request and filters search queries based on these identifiers.
  - Supports exclusion of specified resource types.

