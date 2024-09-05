===
API
===

.. THE FOLLOWING IS AN EXAMPLE

.. see https://sphinxcontrib-httpdomain.readthedocs.io/en/stable/
.. for api specific directives

.. .. http:get:: /users/(int:user_id)/posts/(tag)

    The posts tagged with `tag` that the user (`user_id`) wrote.

    **Example request**:

    .. code-block:: http

        GET /users/123/posts/web HTTP/1.1
        Host: example.com
        Accept: application/json, text/javascript

    **Example response**:

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        [
            {
              "post_id": 12345,
              "author_id": 123,
              "tags": ["server", "web"],
              "subject": "I tried Nginx"
            },
            {
              "post_id": 12346,
              "author_id": 123,
              "tags": ["html5", "standards", "web"],
              "subject": "We go to HTML 5"
            }
        ]

    :form example: an example formdata parameter

    :query sort: one of ``hit``, ``created-at``
    :query offset: offset number. default is 0
    :query limit: limit number. default is 30
    :reqheader Accept: the response content type depends on
                      :mailheader:`Accept` header
    :reqheader Authorization: optional OAuth token to authenticate
    :resheader Content-Type: this depends on :mailheader:`Accept`
                            header of request
    :statuscode 200: no error
    :statuscode 404: there's no user



General Notes
=============

Arches allows any parameters to be passed in via custom HTTP headers OR via the querystring.
All requests to secure services require users to pass a "Bearer" token in the authentication header

To use a an HTTP header to pass in a parameter use the form:

    .. code-block:: none

        HTTP-X-ARCHES-{upper case parameter name}.

So, for example, these are equivelent requests

    .. code-block:: none

        curl -H "X-ARCHES-FORMAT: json-ld" http://localhost:8000/mobileprojects

        curl http://localhost:8000/mobileprojects?format=json-ld

If both a custom header and querystring with the same name are provided, then the querystring parameter takes precedence.

    In the following example "html" will be used as the value for the "format" parameter.

    .. code-block:: none

        curl -H "X-ARCHES-FORMAT: json-ld" http://localhost:8000/mobileprojects?format=html

.. note:: Querystring parameters are case sensitive.  Behind the scenes, custom header parameters are converted to lower case querystring parameters.

    In the following example there are 3 different parameters ("format", "FORMAT", and "Format") with 3 different values ("html", "json", and "xml") respectively

    .. code-block:: none

        http://localhost:8000/mobileprojects?format=html&FORMAT=json&Format=xml

Register an OAuth Application
=============================

To allow others to connect to your Arches instance, you must create an OAuth client id and add it to your settings.

#. In a browser go to

    .. code-block:: none

        http://<yourdomain:port>/o/applications/

#. Create a new application
#. Fill out the form with a **Name** of your choosing, and set **Client type** and **Authorization grant type** as shown in the image below.

    .. image:: ../../images/oauth-create-client.png

#. Copy the **Client id** and submit the form (you can access this id at any time).
#. In your Arches project's ``settings.py`` or ``settings_local.py`` file, set or add this variable

    .. code-block:: none

        MOBILE_OAUTH_CLIENT_ID = "<your new Client id>"

.. important::

    + Only make one application, though you are technically allowed to make more.
    + An application is "owned" by whichever user created it, and will not be visible to other users.

Authentication
==============

.. .. _auth_old:

    .. http:post:: /auth/get_token *deprecated*

        gets an authorization token given a username and password

        **Example request**:

        .. code-block:: none

            curl -X POST http://localhost:8000/auth/get_token -d "username=admin&password=admin"


        **Example response**:

        .. code-block:: http

            HTTP/1.0 200 OK
            Content-Type: text/plain

            eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM


        .. code-block:: http

            HTTP/1.0 401 Unauthorized
            Content-Type: text/plain
            WWW-Authenticate: Bearer


        :form username: a users username (or email)
        :form password: a users password
        :statuscode 401: there's no user or the user has been deactivated, or the token is malformed or expired


Most Arches API endpoints require an OAuth access token.

OAuth 2.0 is a simple and secure authentication mechanism. It allows applications to acquire an access token for Arches via a quick redirect to the Arches site. Once an application has an access token, it can access a user's resources on Arches. to authenticate with OAuth you must first :ref:`Register an OAuth Application`.

.. _auth:

.. http:post:: /o/token

    gets an OAuth token given a username, password, and client id

    .. note:: You should only make this call once and store the returned token securely. You should not make this call per request or at any other high-frequency interval.

        This token is to be used with clients registered with the "Resource Owner Password Credentials Grant" type
        see :ref:`Register an OAuth Application` for more information on registering an application

        For additional information see https://tools.ietf.org/html/rfc6749#section-4.3


    :form username: a users username (or email)
    :form password: a users password
    :form grant_type: "password"
    :form client_id: the registered applications client id, see :ref:`Register an OAuth Application`
    :statuscode 401: there's no user or the user has been deactivated, or the client id is invalid


    **Example request**:

    .. code-block:: none

        curl -X POST http://localhost:8000/o/token/ -d "username=admin&password=admin&grant_type=password&client_id=onFiQSbPfgZpsUcl2fBvaaEHA58MKHavl3iuSaRf"


    **Example response**:

    .. code-block:: http

        HTTP/1.1 200 OK
        Content-Type: application/json

        {
            "access_token": "TS3pE2bEXRCAkRls4IGKCVVa0Zv6FE",
            "token_type": "Bearer",
            "expires_in": 36000,
            "refresh_token": "y3rzXKf8dXdb25ayMMVIligTkqEKr0",
            "scope": "read write"
        }


    returned when an invalid username or password is supplied

    .. code-block:: http

        HTTP/1.1 401 Unauthorized
        Content-Type: application/json


        {"error_description": "Invalid credentials given.", "error": "invalid_grant"}



    returned when an invalid client id is supplied, or the registerd client is not "public" or the
    grant type used to register the client isn't "Resource Owner Password Credentials Grant"

    .. code-block:: http

        HTTP/1.1 401 Unauthorized
        Content-Type: application/json

        {"error": "invalid_client"}


Concepts
=========

.. http:get:: /rdm/concepts/{uuid:concept instance id}

    gets a single rdm concept instance

    :query format: {"json-ld", "json"} (default is ``json-ld``)
    :query indent: integer number of spaces to indent json output (default is none)
    :query includesubconcepts: option to include sub concepts in the return (default is ``true``)
    :query includeparentconcepts: option to include parent concepts in the return (default is ``true``)
    :query includerelatedconcepts: option to include related concepts in the return (default is ``true``)
    :query depthlimit: limit the number of subconcept layers to return if includesubconcepts is true (default is none)
    :query lang: show subconcept results with specified language first (default is project default language)
    :reqheader Authorization: oAuth token for user authentication, see :ref:`/o/token <auth>`

    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X GET http://localhost:8000/rdm/concepts/{concept instance id}

        curl -H "Authorization: Bearer zo41Q1IMgAW30xOroiCUxjv3yci8Os" -X GET http://localhost:8000/rdm/concepts/5e04c83e-1ae3-42e8-ae31-4f7c25f737a5?format=json&indent=4


    **Example json response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "hassubconcepts": true,
            "id": "5e04c83e-1ae3-42e8-ae31-4f7c25f737a5",
            "legacyoid": "http://www.archesproject.org/5e04c83e-1ae3-42e8-ae31-4f7c25f737a5",
            "nodetype": "Concept",
            "parentconcepts": [{
                "hassubconcepts": true,
                "id": "7b8e4771-2680-4004-9743-40ea78e8c2a9",
                "legacyoid": "http://www.archesproject.org/7b8e4771-2680-4004-9743-40ea78e8c2a9",
                "nodetype": "ConceptScheme",
                "parentconcepts": [],
                "relatedconcepts": [],
                "relationshiptype": "hasTopConcept",
                "subconcepts": [],
                "values": [{
                    "category": "label",
                    "conceptid": "7b8e4771-2680-4004-9743-40ea78e8c2a9",
                    "id": "b18048a9-4814-43f0-bb88-99fa22a42fbe",
                    "language": "en-US",
                    "type": "prefLabel",
                    "value": "DISCO"
                }, {
                    "category": "note",
                    "conceptid": "7b8e4771-2680-4004-9743-40ea78e8c2a9",
                    "id": "16ea8772-d5dd-481d-91a7-c09703718138",
                    "language": "en-US",
                    "type": "scopeNote",
                    "value": "Concept scheme for managing Data Integration for Conservation Science thesauri"
                }, {
                    "category": "identifiers",
                    "conceptid": "7b8e4771-2680-4004-9743-40ea78e8c2a9",
                    "id": "9eaa8a10-e9f2-4ce3-ac8b-c4904097b4c9",
                    "language": "en-US",
                    "type": "identifier",
                    "value": "http://www.archesproject.org/7b8e4771-2680-4004-9743-40ea78e8c2a9"
                }]
            }],
            "relatedconcepts": [],
            "relationshiptype": "",
            "subconcepts": [{
                "hassubconcepts": false,
                "id": "0788acb1-9968-43e8-80f7-37b37e155f95",
                "legacyoid": "http://www.archesproject.org/0788acb1-9968-43e8-80f7-37b37e155f95",
                "nodetype": "Concept",
                "parentconcepts": [{
                    "hassubconcepts": false,
                    "id": "5e04c83e-1ae3-42e8-ae31-4f7c25f737a5",
                    "legacyoid": "http://www.archesproject.org/5e04c83e-1ae3-42e8-ae31-4f7c25f737a5",
                    "nodetype": "Concept",
                    "parentconcepts": [],
                    "relatedconcepts": [],
                    "relationshiptype": "narrower",
                    "subconcepts": [],
                    "values": []
                }],
                "relatedconcepts": [],
                "relationshiptype": "narrower",
                "subconcepts": [],
                "values": [{
                    "category": "label",
                    "conceptid": "0788acb1-9968-43e8-80f7-37b37e155f95",
                    "id": "dd5c6d39-7bc4-438e-abe2-544b8ae06864",
                    "language": "en-US",
                    "type": "prefLabel",
                    "value": "Artist"
                }, {
                    "category": "identifiers",
                    "conceptid": "0788acb1-9968-43e8-80f7-37b37e155f95",
                    "id": "5f355975-29a7-4a53-8260-4093d63c1967",
                    "language": "en-US",
                    "type": "identifier",
                    "value": "http://www.archesproject.org/0788acb1-9968-43e8-80f7-37b37e155f95"
                }]
            }],
            "values": [{
                "category": "label",
                "conceptid": "5e04c83e-1ae3-42e8-ae31-4f7c25f737a5",
                "id": "b75ca80a-3128-421d-ae2b-aacb7d12bbc7",
                "language": "en-US",
                "type": "prefLabel",
                "value": "DISCO Actor Types"
            }, {
                "category": "identifiers",
                "conceptid": "5e04c83e-1ae3-42e8-ae31-4f7c25f737a5",
                "id": "79d2e5d2-91fc-435d-869a-042c994d3481",
                "language": "en-US",
                "type": "identifier",
                "value": "http://www.archesproject.org/5e04c83e-1ae3-42e8-ae31-4f7c25f737a5"
            }]
        }


Resources
=========

.. http:get:: /resources/

    gets a paged list of resource instance ids in json-ld format

    :query page: number specifying the page of results to return

    **Example request**:

    .. code-block:: none

        curl -X GET http://localhost:8000/resources/

        curl -X GET http://localhost:8000/resources/?page=2


    **Example response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "@context": "https://www.w3.org/ns/ldp/",
            "@id": "",
            "@type": "ldp:BasicContainer",
            "ldp:contains": [
                "http://localhost:8000/resources/00000000-0000-0000-0000-000000000100",
                "http://localhost:8000/resources/00000000-0000-0000-0000-000000000101",
                "http://localhost:8000/resources/000ee2fe-4568-457b-960c-3e1ec3f53e10",
                "http://localhost:8000/resources/000fa53f-0f06-4648-a960-c42b8accd235",
                "http://localhost:8000/resources/00131129-7451-435d-aab9-33eb9031e6d1",
                "http://localhost:8000/resources/001b6c4b-f906-4df2-9fcd-b9fda95eed95",
                "http://localhost:8000/resources/0032990e-f8d6-4a7b-8032-d90d3c764b40",
                "http://localhost:8000/resources/003619ca-5fa7-4e75-b3b7-a62f40fe9419",
                "http://localhost:8000/resources/00366caa-3c00-4909-851d-0d650e62f820",
                "http://localhost:8000/resources/003874d7-8e73-4323-bddf-b893651e22c1",
                "http://localhost:8000/resources/003e56a0-d0eb-485f-b975-61faf2f22755",
                "http://localhost:8000/resources/0043a0be-c7be-4a35-9f6c-0ba80269caf4",
                "http://localhost:8000/resources/0060f35d-47a7-4f22-aaf3-fa2d0bd493f7",
                "http://localhost:8000/resources/0069dad8-41b6-4cad-8e54-f72fe8093550",
                "http://localhost:8000/resources/0069db14-a0c1-470e-abf7-eda7b56bf012"
            ]
        }


.. http:get:: /resources/{uuid:resource instance id}

    gets a single resource instance

    :query format: {"json-ld", "json", "arches-json"} (default is ``json-ld``)
    :query hidden: hide hidden nodes {"true", "false"} (default is ``true``)
    :query indent: integer number of spaces to indent json output (default is ``None``)
    :reqheader Authorization: OAuth token for user authentication, see :ref:`/o/token <auth>`
    :reqheader Accept: optional alternative to "format", {"application/xml", "application/json", "application/ld+json"}

    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X GET http://localhost:8000/resources/{resource instance id}

        curl -H "Authorization: Bearer zo41Q1IMgAW30xOroiCUxjv3yci8Os" -X GET http://localhost:8000/resources/00131129-7451-435d-aab9-33eb9031e6d1?format=json&indent=4


    **Example json response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "business_data": {
                "resources": [
                    {
                        "tiles": [
                            {
                                "data": {
                                    "e4b37f8a-343a-11e8-ab89-dca90488358a": "203 Boultham Park Road"
                                    "e4b4b7f5-343a-11e8-a681-dca90488358a": null,
                                },
                                "provisionaledits": null,
                                "parenttile_id": null,
                                "nodegroup_id": "e4b37f8a-343a-11e8-ab89-dca90488358a",
                                "sortorder": 0,
                                "resourceinstance_id": "99131129-7451-435d-aab9-33eb9031e6d1",
                                "tileid": "b72225a9-4e3d-47ee-8d94-52316469bc3f"
                            },
                            {
                                "data": {
                                    "e4b3f15c-343a-11e8-a26b-dca90488358a": null,
                                    "e4b4ca3d-343a-11e8-ab73-dca90488358a": {
                                        "type": "FeatureCollection",
                                        "features": [
                                            {
                                                "geometry": {
                                                    "type": "Point",
                                                    "coordinates": [
                                                        -0.559288403624841,
                                                        53.2132233001817
                                                    ]
                                                },
                                                "type": "Feature",
                                                "id": "c036e50a-4959-4b6f-93d0-2c03068c0948",
                                                "properties": {}
                                            }
                                        ]
                                    }
                                },
                                "provisionaledits": null,
                                "parenttile_id": "4e40e6f3-8252-4439-831d-c371655cc4eb",
                                "nodegroup_id": "e4b3f15c-343a-11e8-a26b-dca90488358a",
                                "sortorder": 0,
                                "resourceinstance_id": "99131129-7451-435d-aab9-33eb9031e6d1",
                                "tileid": "65199340-32c3-4936-a09e-7c5143552d15"
                            },
                            {
                                "data": {
                                    "e4b386eb-343a-11e8-82ef-dca90488358a": "Detached house built by A B Sindell"
                                },
                                "provisionaledits": null,
                                "parenttile_id": "8870d2d6-e179-4321-a8bb-543fd2db63c6",
                                "nodegroup_id": "e4b386eb-343a-11e8-82ef-dca90488358a",
                                "sortorder": 0,
                                "resourceinstance_id": "99131129-7451-435d-aab9-33eb9031e6d1",
                                "tileid": "04bb7bef-1e6e-4228-bd87-3f0a129514a8"
                            }
                        ],
                        "resourceinstance": {
                            "graph_id": "e4b3562b-343a-11e8-b509-dca90488358a",
                            "resourceinstanceid": "99131129-7451-435d-aab9-33eb9031e6d1",
                            "legacyid": "99131129-7451-435d-aab9-33eb9031e6d1"
                        }
                    }
                ]
            }
        }

.. http:put:: /resources/{uuid: graph id}/{uuid:resource instance id}

    .. note::
        Instead of identifying a graph by a UUID, one can also identify a graph by by a slug identifier. 
        To get or set the slug for the graph, navigate to the root node of the :ref:`Graph Designer`. A request using a slug identifier for a graph looks like:
        ``PUT /resources/{string: graph slug}/{uuid:resource instance id}``


    Updates a single resource instance

    :query format: {"json-ld", "arches-json"} (default is ``json-ld``)
    :query indent: number of spaces to indent json output (default is ``None``)
    :reqheader Authorization: OAuth token for user authentication, see :ref:`/o/token <auth>`
    :reqheader Accept: optional alternative to "format", {"application/json", "application/ld+json"}

    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X PUT -d {data in json-ld format} http://localhost:8000/resources/{graph id}/{resource instance id}

        curl -H "Authorization: Bearer zo41Q1IMgAW30xOroiCUxjv3yci8Os" -X PUT \
        -d '{
            "@id": "http://localhost:8000/resource/47a1830c-74ec-11e8-bff6-14109fd34195",
            "@type": [
                "http://www.cidoc-crm.org/cidoc-crm/E18_Physical_Thing",
                "http://localhost:8000/graph/ab74af76-fa0e-11e6-9e3e-026d961c88e6"
            ],
            "http://www.cidoc-crm.org/cidoc-crm/P140i_was_attributed_by": {
                "@id": "http://localhost:8000/tile/1f7b4c8f-9932-47e4-9ec5-0284c77d893c/node/677f236e-09cc-11e7-8ff7-6c4008b05c4c",
                "@type": "http://www.cidoc-crm.org/cidoc-crm/E15_Identifier_Assignment",
                "http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by": [
                    {
                        "@id": "http://localhost:8000/tile/6efb8ac0-623c-47cb-9846-4a489c153683/node/677f303d-09cc-11e7-9aa6-6c4008b05c4c",
                        "@type": "http://www.cidoc-crm.org/cidoc-crm/E41_Appellation",
                        "http://www.cidoc-crm.org/cidoc-crm/P2_has_type": {
                            "@id": "http://localhost:8000/tile/6efb8ac0-623c-47cb-9846-4a489c153683/node/677f39a8-09cc-11e7-834a-6c4008b05c4c",
                            "@type": "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
                            "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "ecb20ae9-a457-4011-83bf-1c936e2d6b6a"
                        },
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "Claudio"
                    },
                    {
                        "@id": "http://localhost:8000/tile/b53f2aaa-348b-4b73-9ff9-195090038c8b/node/677f303d-09cc-11e7-9aa6-6c4008b05c4c",
                        "@type": "http://www.cidoc-crm.org/cidoc-crm/E41_Appellation",
                        "http://www.cidoc-crm.org/cidoc-crm/P2_has_type": {
                            "@id": "http://localhost:8000/tile/b53f2aaa-348b-4b73-9ff9-195090038c8b/node/677f39a8-09cc-11e7-834a-6c4008b05c4c",
                            "@type": "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
                            "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "81dd62d2-6701-4195-b74b-8057456bba4b"
                        },
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "Alejandro"
                    }
                ],
                "http://www.cidoc-crm.org/cidoc-crm/P2_has_type": {
                    "@id": "http://localhost:8000/tile/e818ecc5-8bde-4978-baca-2206a5bbf509/node/677f2c0f-09cc-11e7-b412-6c4008b05c4c",
                    "@type": "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "e4699732-efee-46c0-87e1-3f0a930a43db"
                }
            }
        }' \
        'http://localhost:8000/resources/00131129-7451-435d-aab9-33eb9031e6d1?format=json-ld&indent=4'


    **Example json response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "@id": "http://localhost:8000/resource/47a1830c-74ec-11e8-bff6-14109fd34195",
            "@type": [
                "http://www.cidoc-crm.org/cidoc-crm/E18_Physical_Thing",
                "http://localhost:8000/graph/ab74af76-fa0e-11e6-9e3e-026d961c88e6"
            ],
            "http://www.cidoc-crm.org/cidoc-crm/P140i_was_attributed_by": {
                "@id": "http://localhost:8000/tile/1f7b4c8f-9932-47e4-9ec5-0284c77d893c/node/677f236e-09cc-11e7-8ff7-6c4008b05c4c",
                "@type": "http://www.cidoc-crm.org/cidoc-crm/E15_Identifier_Assignment",
                "http://www.cidoc-crm.org/cidoc-crm/P1_is_identified_by": [
                    {
                        "@id": "http://localhost:8000/tile/6efb8ac0-623c-47cb-9846-4a489c153683/node/677f303d-09cc-11e7-9aa6-6c4008b05c4c",
                        "@type": "http://www.cidoc-crm.org/cidoc-crm/E41_Appellation",
                        "http://www.cidoc-crm.org/cidoc-crm/P2_has_type": {
                            "@id": "http://localhost:8000/tile/6efb8ac0-623c-47cb-9846-4a489c153683/node/677f39a8-09cc-11e7-834a-6c4008b05c4c",
                            "@type": "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
                            "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "ecb20ae9-a457-4011-83bf-1c936e2d6b6a"
                        },
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "Claudio"
                    },
                    {
                        "@id": "http://localhost:8000/tile/b53f2aaa-348b-4b73-9ff9-195090038c8b/node/677f303d-09cc-11e7-9aa6-6c4008b05c4c",
                        "@type": "http://www.cidoc-crm.org/cidoc-crm/E41_Appellation",
                        "http://www.cidoc-crm.org/cidoc-crm/P2_has_type": {
                            "@id": "http://localhost:8000/tile/b53f2aaa-348b-4b73-9ff9-195090038c8b/node/677f39a8-09cc-11e7-834a-6c4008b05c4c",
                            "@type": "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
                            "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "81dd62d2-6701-4195-b74b-8057456bba4b"
                        },
                        "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "Alejandro"
                    }
                ],
                "http://www.cidoc-crm.org/cidoc-crm/P2_has_type": {
                    "@id": "http://localhost:8000/tile/e818ecc5-8bde-4978-baca-2206a5bbf509/node/677f2c0f-09cc-11e7-b412-6c4008b05c4c",
                    "@type": "http://www.cidoc-crm.org/cidoc-crm/E55_Type",
                    "http://www.w3.org/1999/02/22-rdf-syntax-ns#value": "e4699732-efee-46c0-87e1-3f0a930a43db"
                }
            }
        }

.. http:delete:: /resources/{uuid:resource instance id}

    deletes a single resource instance

    :reqheader Authorization: OAuth token for user authentication, see :ref:`/o/token <auth>`

    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X DELETE http://localhost:8000/resources/{resource instance id}

        curl -H "Authorization: Bearer zo41Q1IMgAW30xOroiCUxjv3yci8Os" -X DELETE http://localhost:8000/resources/00131129-7451-435d-aab9-33eb9031e6d1


    **Example response**:

    .. code-block:: http

        HTTP/1.0 200 OK


Activity Stream
===============

.. http:get:: /history/

    gets a JSON-LD representation of the collection that comprises the changes made (Create, Update, Delete) to Arches resources.

    :reqheader Authorization: OAuth token for user authentication, see :ref:`/o/token <auth>`

    **Example request**:

    .. code-block:: none

        curl -X GET http://localhost:8000/history/

    **Example response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "OrderedCollection",
            "id": "http://localhost:8000/history/",
            "totalItems": 7,
            "first": {
                "type": "OrderedCollectionPage",
                "id": "http://localhost:8000/history/1"
            },
            "last": {
                "type": "OrderedCollectionPage",
                "id": "http://localhost:8000/history/1"
            }
        }


.. http:get:: /history/{int: page number}

    gets a single 'OrderedCollectionPage' JSON-LD representation for a given page number

    :reqheader Authorization: OAuth token for user authentication, see :ref:`/o/token <auth>`

    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X GET http://localhost:8000/history/{page number}

        curl -H "Authorization: Bearer zo41Q1IMgAW30xOroiCUxjv3yci8Os" -X GET http://localhost:8000/history/1

    **Example json response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "OrderedCollectionPage",
            "id": "http://localhost:8000/history/1",
            "partOf": {
                "totalItems": 7,
                "type": "OrderedCollection",
                "id": "http://localhost:8000/history/"
            },
            "orderedItems": [
                {
                    "endTime": "2019-06-20T17:38:56Z",
                    "type": "Create",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": null,
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/47b179f0-9382-11e9-b0f5-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E33_Linguistic_Object"
                    }
                },
                {
                    "endTime": "2019-06-20T17:38:57Z",
                    "type": "Update",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": "admin",
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/47b179f0-9382-11e9-b0f5-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E33_Linguistic_Object"
                    }
                },
                {
                    "endTime": "2019-06-20T17:39:04Z",
                    "type": "Update",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": "admin",
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/47b179f0-9382-11e9-b0f5-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E33_Linguistic_Object"
                    }
                },
                {
                    "endTime": "2019-06-20T17:39:13Z",
                    "type": "Create",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": null,
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/514796f2-9382-11e9-9e60-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object"
                    }
                },
                {
                    "endTime": "2019-06-20T17:39:13Z",
                    "type": "Update",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": "admin",
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/514796f2-9382-11e9-9e60-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object"
                    }
                },
                {
                    "endTime": "2019-06-20T17:39:15Z",
                    "type": "Update",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": "admin",
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/47b179f0-9382-11e9-b0f5-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E33_Linguistic_Object"
                    }
                },
                {
                    "endTime": "2019-06-20T17:39:24Z",
                    "type": "Update",
                    "actor": {
                        "url": "http://localhost:8000/user/1",
                        "tag": "admin",
                        "type": "Person",
                        "name": ", "
                    },
                    "object": {
                        "url": "http://localhost:8000/resources/47b179f0-9382-11e9-b0f5-0242ac120003",
                        "type": "http://www.cidoc-crm.org/cidoc-crm/E33_Linguistic_Object"
                    }
                }
            ]
        }


Mobile Projects
===============

.. http:get:: /mobileprojects

    get a list of mobile data collection projects that a user has been invited to participate in


    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X GET http://localhost:8000/mobileprojects

        curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM" -X GET http://localhost:8000/mobileprojects


    **Example response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        [
            {
                "active": true,
                "bounds": "MULTIPOLYGON EMPTY",
                "cards": [],
                "createdby_id": 1,
                "datadownloadconfig": {
                    "count": 1000,
                    "custom": null,
                    "download": false,
                    "resources": []
                },
                "description": "A description of this project.",
                "enddate": "2018-03-16",
                "groups": [
                    6
                ],
                "id": "e3d95999-2323-11e8-894b-14109fd34195",
                "lasteditedby_id": 1,
                "name": "Forbidden Project",
                "startdate": "2018-03-04",
                "tilecache": "",
                "users": [
                    1
                ]
            }
        ]


    :reqheader Authorization: JWT (JSON web token) for user authentication, see :ref:`/auth/get_token <auth>`


GeoJSON
=========

.. http:get:: /geojson

    returns a GeoJSON representation of resource instance data; this will include metadata properties when using paging for "_page" (number) and "_lastPage" (boolean).  Returned features will include integer ids that are only assured to be unique per request.

    NOTE: when not using the "use_uuid_names" parameter, field names will use the export field name provided for a given node (via the Graph Designer).
    If the export field name is not defined, the API will attempt to create a suitable field name from the node name.
    Property names that clash as a result of the above, or shortening via "field_name_length" will have their values joined together.

    WARNING: including primary names has a big impact on performance and is best defered to an additional request

    :query resourceid: optional comma delimited list of resource instance UUIDs to filter feature data on
    :query nodeids: optional comma delimited list of node UUIDs to filter feature data on
    :query tileid: optional tile UUID to filter feature data on
    :query nodegroups: optional comma delimited list of nodegroup UUIDs from which to include tile data as properties.
    :query precision: optional number of decimal places returned in coordinate values; used to constrain resultant data volume
    :query field_name_length: optional number to limit property field length to
    :query use_uuid_names: include this parameter to return tile property names as node UUIDs.
    :query include_primary_name: include this parameter to include resource instance primary names in feature properties.
    :query use_display_values: include this parameter to return tile values processed to be human readable
    :query include_geojson_link: include this parameter to include a link to this specific feature in its properties fit for reuse later
    :query indent: optional number of spaces with which to indent the JSON return (ie "pretty print")
    :query type: optional geometry type name to filter features on
    :query limit: optional number of tiles to process; used to page data. NOTE: as paging is per tile, the count of features in the response may differ from this limit value
    :query page: optional number of page (starting with 1) to return; used in conjunction with "limit"

    **Example request**:

    .. code-block:: none

        curl -X GET http://localhost:8000/geojson?nodegroups=8d41e4ab-a250-11e9-87d1-00224800b26d,8d41e4c0-a250-11e9-a7e3-00224800b26d&nodeid=8d41e4d6-a250-11e9-accd-00224800b26d&use_display_values=true&indent=2&limit=3


    **Example response**:

    .. code-block:: http

        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "_lastPage": false,
            "_page": 1,
            "features": [{
                "geometry": {
                    "coordinates": [
                        -0.09160837,
                        51.529378348
                    ],
                    "type": "Point"
                },
                "id": 1,
                "properties": {
                    "application_type": "Enquiry",
                    "consultation_status": "Dormant",
                    "consultation_type": "Post-Application",
                    "development_type": "Mixed Use",
                    "name": "Consultation for 93 Mendota Alley",
                    "resourceinstanceid": "aa7ecf38-ab81-4e08-bb74-cfdd1e339ea2",
                    "tileid": "4e4d8fe8-3ee9-4ddc-9613-fffc1511bd58"
                },
                "type": "Feature"
            }, {
                "geometry": {
                    "coordinates": [
                        -0.090902277,
                        51.533642427
                    ],
                    "type": "Point"
                },
                "id": 2,
                "properties": {
                    "application_type": "Listed Building Consent",
                    "consultation_status": "Completed",
                    "consultation_type": "Condition Application",
                    "development_type": "Land restoration",
                    "name": "Consultation for 57359 Fieldstone Way",
                    "resourceinstanceid": "2cf195f8-805b-4f97-9133-cbd94bf5a01f",
                    "tileid": "6e3009d4-4022-4510-8e42-504b5bc20b74"
                },
                "type": "Feature"
            }, {
                "geometry": {
                    "coordinates": [
                        -0.088202575,
                        51.533347841
                    ],
                    "type": "Point"
                },
                "id": 3,
                "properties": {
                    "application_type": "Listed Building Consent",
                    "consultation_status": "Aborted",
                    "consultation_type": "Post-Application",
                    "development_type": "Road construction",
                    "name": "Consultation for 3660 Kim Court",
                    "resourceinstanceid": "eefa863a-53e4-404a-89b4-6213b46b2b55",
                    "tileid": "99395221-dd7f-4a06-8d87-5f5703501ab5"
                },
                "type": "Feature"
            }],
            "type": "FeatureCollection"
        }

Spatial View Management
=======================

.. http:get:: /api/spatialviews

    Get a list of spatial views that the user has permission to see, based upon the geometry nodes that they have access to


    **Example request**:

    .. code-block:: none

        curl -H "Authorization: Bearer {token}" -X GET http://localhost:8000/api/spatialviews

        curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM" -X GET http://localhost:8000/api/spatialviews

    **Example response**:

    .. code-block:: http
            
        HTTP/1.0 200 OK
        Content-Type: application/json

        [
            {
                "attributenodes": [
                    {
                        "description": "name",
                        "nodeid": "bee90060-1cf8-11ef-971a-0242ac130005"
                    }
                ],
                "description": "test_description",
                "geometrynodeid": "95b2c8de-1cf8-11ef-971a-0242ac130005",
                "isactive": true,
                "ismixedgeometrytypes": false,
                "language": "en",
                "schema": "public",
                "slug": "spatialviews_test",
                "spatialviewid": "3d031564-3304-11ef-af57-0242ac150006"
            }
        ]

.. http:get:: /api/spatialviews/{uuid:spatial view id}

    Get a single spatial view by its UUID  

    **Example request**:

    .. code-block:: none

        curl  -X GET http://localhost:8000/api/spatialviews/3d031564-3304-11ef-af57-0242ac150006

        curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM" -X GET http://localhost:8000/api/spatialviews/3d031564-3304-11ef-af57-0242ac150006

    **Example response**:

    .. code-block:: http
            
        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "attributenodes": [
                {
                    "description": "name",
                    "nodeid": "bee90060-1cf8-11ef-971a-0242ac130005"
                }
            ],
            "description": "test_description",
            "geometrynodeid": "95b2c8de-1cf8-11ef-971a-0242ac130005",
            "isactive": true,
            "ismixedgeometrytypes": false,
            "language": "en",
            "schema": "public",
            "slug": "spatialviews_test",
            "spatialviewid": "3d031564-3304-11ef-af57-0242ac150006"
        }

.. http:post:: /api/spatialviews

    Create a new spatial view. The user must be a member of the Application Admin group.

    :query description: description of the spatial view
    :query geometrynodeid: UUID of the geometry node that the spatial view is based on
    :query isactive: boolean indicating if the spatial view is active
    :query ismixedgeometrytypes: boolean indicating if the spatial view should create a mixed geometry type view
    :query language: language of the spatial view (must be a valid language code assigned to a published graph that the geometry node belongs to)
    :query schema: database schema of the spatial view (this must already have been created)
    :query slug: slug of the spatial view (this must be unique in the system)
    :query attributenodes: list of attribute nodes that the spatial view should include (each attribute node must have a nodeid and description)

    **Example request**:

    .. code-block:: none

        curl -X POST -d "description=test_description&geometrynodeid=95b2c8de-1cf8-11ef-971a-0242ac130005&isactive=true&ismixedgeometrytypes=false&language=en&schema=public&slug=spatialviews_test" http://localhost:8000/api/spatialviews

        curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM" -X POST \
        -d "{
            'description': 'test_description',
            'geometrynodeid': '95b2c8de-1cf8-11ef-971a-0242ac130005',
            'isactive': true,
            'ismixedgeometrytypes': false,
            'language': 'en',
            'schema': 'public',
            'slug': 'spatialviews_test',
            'attributenodes': [
                {
                    'description': 'name',
                    'nodeid': 'bee90060-1cf8-11ef-971a-0242ac130005'
                }
            ] 
        }" http://localhost:8000/api/spatialviews

    **Example response**:

    .. code-block:: http
            
        HTTP/1.0 201 Created
        Content-Type: application/json

        {
            "attributenodes": [
                {
                    "description": "name",
                    "nodeid": "bee90060-1cf8-11ef-971a-0242ac130005"
                }
            ],
            "description": "test_description",
            "geometrynodeid": "95b2c8de-1cf8-11ef-971a-0242ac130005",
            "isactive": true,
            "ismixedgeometrytypes": false,
            "language": "en",
            "schema": "public",
            "slug": "spatialviews_test",
            "spatialviewid": "3d031564-3304-11ef-af57-0242ac150006"
        }

.. http:put:: /api/spatialviews/{uuid:spatial view id}

    Update a spatial view. The user must be a member of the Application Admin group.

    :query spatialviewid: UUID of the spatial view
    :query description: description of the spatial view
    :query geometrynodeid: UUID of the geometry node that the spatial view is based on
    :query isactive: boolean indicating if the spatial view is active
    :query ismixedgeometrytypes: boolean indicating if the spatial view should create a mixed geometry type view
    :query language: language of the spatial view (must be a valid language code assigned to a published graph that the geometry node belongs to)
    :query schema: database schema of the spatial view (this must already have been created)
    :query slug: slug of the spatial view (this must be unique in the system)
    :query attributenodes: list of attribute nodes that the spatial view should include (each attribute node must have a nodeid and description)

    **Example request**:

    .. code-block:: none

        curl -X PUT -d "description=test_description&geometrynodeid=95b2c8de-1cf8-11ef-971a-0242ac130005&isactive=true&ismixedgeometrytypes=false&language=en&schema=public&slug=spatialviews_test" http://localhost:8000/api/spatialviews/3d031564-3304-11ef-af57-0242ac150006

        curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM" -X PUT \
        -d "{
            'description': 'test_description',
            'geometrynodeid': '95b2c8de-1cf8-11ef-971a-0242ac130005',
            'isactive': false,
            'ismixedgeometrytypes': false,
            'language': 'en',
            'schema': 'public',
            'slug': 'spatialviews_test',
            'attributenodes': [
                {
                    'description': 'name',
                    'nodeid': 'bee90060-1cf8-11ef-971a-0242ac130005'
                }
            ]
        }" http://localhost:8000/api/spatialviews/3d031564-3304-11ef-af57-0242ac150006

    **Example response**:

    .. code-block:: http
            
        HTTP/1.0 200 OK
        Content-Type: application/json

        {
            "spatialviewid": "3d031564-3304-11ef-af57-0242ac150006",
            "description": "test_description",
            "geometrynodeid": "95b2c8de-1cf8-11ef-971a-0242ac130005",
            "isactive": false,
            "ismixedgeometrytypes": false,
            "language": "en",
            "schema": "public",
            "slug": "spatialviews_test",
            "attributenodes": [
                {
                    "description": "name",
                    "nodeid": "bee90060-1cf8-11ef-971a-0242ac130005"
                }
            ]
        }

.. http:delete:: /api/spatialviews/{uuid:spatial view id}

    Delete a spatial view. The user must be a member of the Application Admin group.

    **Example request**:

    .. code-block:: none

        curl -X DELETE http://localhost:8000/api/spatialviews/3d031564-3304-11ef-af57-0242ac150006

        curl -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiJiMDhmODZhZi0zNWRhLTQ4ZjItOGZhYi1jZWYzOTA0NjYwYmQifQ.-xN_h82PHVTCMA9vdoHrcZxH-x5mb11y1537t3rGzcM" -X DELETE http://localhost:8000/api/spatialviews/3d031564-3304-11ef-af57-0242ac150006

    **Example response**:

    .. code-block:: http
            
        HTTP/1.0 204 No Content