.. _node-value-api:

Updating one node value (Arches 7.6)
====================================

``POST /api/node_value/`` updates one node value in one tile. This page
describes Arches **7.6.24**. The path is relative to the deployment's base
URL. The route uses ``arches.app.views.api.NodeValue.post``, which reads
form fields from ``request.POST`` and calls
``TileProxyModel.update_node_value``. Send form data, not a raw JSON body.

A request contains one ``nodeid``. Changing two nodes requires two calls.
The full-tile ``POST /api/tiles/<tile-uuid>`` is a separate API.

Authentication and permissions
------------------------------

Use an authenticated Arches session or an OAuth bearer token obtained through
:ref:`/o/token <auth>` for a user in the **Resource Editor** group. The
7.6.24 view is CSRF exempt, so this particular
POST needs no CSRF token even with session authentication. Other routes can
have different CSRF rules. Keep cookies and tokens secret.

The user also needs ``write_nodegroup`` permission on the target nodegroup
and permission to edit the resource. A Resource Reviewer calling this route
must pass the Resource Editor group check too. Anonymous callers and users
outside that group get HTTP 403 from the group decorator. Nodegroup and
resource permission failures return HTTP 403 from the view.

node_value form fields
----------------------

.. list-table:: Fields read by ``NodeValue.post``
   :header-rows: 1
   :widths: 19 22 59

   * - Field
     - Existing-tile update
     - Meaning
   * - ``nodeid``
     - Required
     - UUID of one node in the resource's graph. A missing or unknown node
       returns 404. Resolve it from model metadata.
   * - ``tileid``
     - Required for a safe update
     - UUID of this tile instance. Omission or an unknown UUID can enter
       the tile creation path.
   * - ``resourceinstanceid``
     - Supply and verify
     - Resource UUID, used when no existing tile is found. For an existing
       tile, the view does **not** compare it with the tile's resource ID.
       Omitting both a usable tile ID and resource ID can create a resource.
   * - ``data``
     - Required for a value update
     - Form string transformed by the node's datatype. Missing data becomes
       ``None`` before conversion; that is not a documented clearing method.
   * - ``format``
     - Optional
     - Passed to the datatype's ``transform_value_for_tile`` method.
       Its effect is datatype specific; omit it for the string examples.
   * - ``operation``
     - Optional
     - Only ``append`` has a special path, and only for an existing tile:
       the view calls that datatype's ``update`` method. Omit for replacement.
       Not every datatype supports append.
   * - ``transaction_id``
     - Optional
     - UUID forwarded to tile save and its edit log. Use a new UUID to
       correlate history entries for one logical edit.

Finding the node and tile
-------------------------

Node UUIDs belong to a resource model and may vary between models, versions,
and deployments. To resolve an alias such as ``name_label`` or
``name_content`` in the **resource's own graph**:

1. Read ``graph.graphid`` from
   ``GET /api/resource_report/<resource-uuid>``.
2. Fetch ``GET /graphs/<graph-uuid>?cards=false``. Its ``graph.nodes``
   contains ``alias``, ``nodeid``, ``nodegroup_id``, and ``datatype``.
3. Require exactly one alias match. Stop on zero or multiple matches.
   Check that any cached node metadata belongs to this graph.

Fetch ``GET /resource/<resource-uuid>/tiles?nodeid=<node-uuid>``. Its
``tiles`` array is filtered by the nodegroup and read permissions. A
nodegroup can have multiple tiles on one resource: choose by contents,
parent tile, or another application-specific criterion. Never silently
take the first. Zero matches can also mean the caller lacks read access.
Then read ``GET /api/tiles/<tile-uuid>`` and verify both
``resourceinstance_id`` and ``nodegroup_id`` before POST.

A tile UUID identifies one tile instance, not every resource using the same
model. If no tile exists, the 7.6.24 helper can create a blank tile and
parent tiles. Supply an existing ``resourceinstanceid`` and omit
``tileid`` only when creation is intentional. This route cannot select
a particular parent or repeating nodegroup instance for creation; use
the tile API or resource editor for that case. An unknown tile UUID can
also fall through to creation.

Datatype-aware values
---------------------

``data`` is a form field even when its value is JSON text. Inspect the
target node's datatype and configuration.

* ``string``: ordinary text such as ``Example value`` becomes a
  language-keyed object using the active language. For an explicit
  multilingual value, submit JSON text as the form value:

  .. code-block:: json

      {"en":{"direction":"ltr","value":"Example value"}}

  The transform parses and stores the object. Preserve other language
  entries when editing one language; supplying only ``en`` replaces
  the whole node value.
* ``concept``: a concept **value UUID** as text,
  ``<concept-value-uuid>``. This differs from the node UUID. Label lookup
  is also supported, but a UUID avoids ambiguous labels.
* ``concept-list``: comma-separated concept value UUIDs in one form
  field, for example
  ``<concept-value-uuid-1>,<concept-value-uuid-2>``. It becomes a list.
  Do not send a JSON array to this transform.
* ``number``: decimal text such as ``12.5``. Digit-only text becomes an
  integer; other numeric text becomes a float.
* ``date``: text matching an instance-configured ``DATE_FORMATS`` format
  or ``DATE_IMPORT_EXPORT_FORMAT``. The transform returns a timezone-aware
  ISO value. Confirm the target deployment's accepted formats.

Provisional edits and review
----------------------------

The endpoint calls ``Tile.save(request=request)``. A Resource Reviewer
writes authoritative ``tile.data``. For an ordinary Resource Editor, the
save calls ``apply_provisional_edit``: the proposal goes into
``tile.provisionaledits`` under that editor's user ID with
``status: "review"``; the prior authoritative data remains in ``tile.data``.
The save also writes an edit-log entry. Inserting JSON directly into
``provisionaledits`` does not run this complete workflow.

The editor's resource editor can show the proposal while other users see
the approved value. A reviewer can find pending edits in search using the
Q/A filter, open the resource editor, inspect the proposal, and accept or
decline it. Acceptance promotes it to authoritative data.

HTTP 200 means the save completed, **not** that the proposal was approved.
The JSON response is a serialized tile. Inspect ``data`` and
``provisionaledits`` (or read the tile again). A pending proposal appears
at ``provisionaledits[<editor-user-id>].value`` with
``status: "review"``. Do not infer approval from HTTP status alone.

Examples
--------

Resolve and verify the node and tile first. Replace one string value
using an OAuth token for an authorized user:

.. code-block:: console

    curl -X POST '<base-url>/api/node_value/' \
      -H 'Authorization: Bearer <access-token>' \
      --data-urlencode 'resourceinstanceid=<resource-uuid>' \
      --data-urlencode 'nodeid=<node-uuid>' \
      --data-urlencode 'tileid=<tile-uuid>' \
      --data-urlencode 'data=Example value'

Submit a multilingual object **as the form field**, not the request body:

.. code-block:: console

    curl -X POST '<base-url>/api/node_value/' \
      -H 'Authorization: Bearer <access-token>' \
      --data-urlencode 'resourceinstanceid=<resource-uuid>' \
      --data-urlencode 'nodeid=<node-uuid>' \
      --data-urlencode 'tileid=<tile-uuid>' \
      --data-urlencode 'data={"en":{"direction":"ltr","value":"Example value"}}'

This Python example begins with a resource UUID and alias. It stops for
missing or ambiguous nodes and tiles and checks tile ownership before POST.
Supply the bearer token through an environment variable.

.. code-block:: python

    import os
    import uuid
    import requests

    base_url = "<base-url>".rstrip("/")
    resource_id = "<resource-uuid>"
    alias = "name_label"
    new_value = "Example value"

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {os.environ['ARCHES_ACCESS_TOKEN']}"

    def get_json(path, **params):
        response = session.get(f"{base_url}{path}", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    report = get_json(f"/api/resource_report/{resource_id}")
    graph_id = report["graph"]["graphid"]
    graph = get_json(f"/graphs/{graph_id}", cards="false")["graph"]
    nodes = graph["nodes"]
    nodes = nodes.values() if isinstance(nodes, dict) else nodes
    matches = [node for node in nodes if node.get("alias") == alias]
    if len(matches) != 1:
        raise ValueError(f"Expected one node for {alias!r}; found {len(matches)}")
    node = matches[0]
    node_id = str(node["nodeid"])
    nodegroup_id = str(node.get("nodegroup_id") or node.get("nodegroupid"))

    candidates = get_json(f"/resource/{resource_id}/tiles", nodeid=node_id)["tiles"]
    if len(candidates) != 1:
        raise ValueError(f"Expected one tile; found {len(candidates)}")
    tile_id = str(candidates[0]["tileid"])
    tile = get_json(f"/api/tiles/{tile_id}")
    if (str(tile["resourceinstance_id"]) != resource_id or
            str(tile["nodegroup_id"]) != nodegroup_id):
        raise ValueError("Tile does not belong to this resource and nodegroup")

    response = session.post(
        f"{base_url}/api/node_value/",
        data={
            "resourceinstanceid": resource_id,
            "tileid": tile_id,
            "nodeid": node_id,
            "data": new_value,
            "transaction_id": str(uuid.uuid4()),
        },
        timeout=30,
    )
    response.raise_for_status()
    saved_tile = response.json()
    print(saved_tile["tileid"], saved_tile.get("provisionaledits"))

Changing ``name_content`` too requires a second
``POST /api/node_value/``. A helper may group the calls, but the endpoint
processes one ``nodeid`` per request.

Responses and failure cases
---------------------------

In 7.6.24 the view explicitly returns:

* **200** with the serialized tile after a completed save. Inspect
  ``data`` and ``provisionaledits`` for the outcome.
* **404** with JSON string ``"Node not found"`` for an unknown or missing
  ``nodeid``.
* **403** with JSON string ``"User does not have permission to edit this
  node."`` for failed ``write_nodegroup``, or ``"User is not permitted
  to edit this resource"`` for a failed resource edit check. Group denial,
  including anonymous access, happens before the view and may be non-JSON.

The view has no dedicated 400 response for malformed resource or tile UUIDs,
tile/resource mismatch, or invalid datatype values. Conversion and save
errors may become server errors. An unknown tile UUID can enter the creation
path, and a mismatched ``resourceinstanceid`` does not protect an existing
tile. Validate UUID syntax, graph membership, tile ownership, and datatype
input before POST. A CSRF rejection is not expected for this exempt route
in stock 7.6.24; authentication and permission checks still apply.

Implementation references
-------------------------

The `7.6.24 route <https://github.com/archesproject/arches/blob/7.6.24/arches/urls.py>`_,
`NodeValue view <https://github.com/archesproject/arches/blob/7.6.24/arches/app/views/api.py>`_,
`tile update and save methods <https://github.com/archesproject/arches/blob/7.6.24/arches/app/models/tile.py>`_,
and `datatype transforms <https://github.com/archesproject/arches/tree/7.6.24/arches/app/datatypes>`_
are the source for this page. Behavior in other releases is not asserted.
