Arches Search Components Documentation
======================================

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

