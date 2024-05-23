.. _creating_new_map_layers_reference:

Creating New Map Layers
#######################

A developer can add new layers to the map by registering them through the command line interface.

New map layers can come from many different geospatial sources -- from shapefiles to GeoTIFFs to external Web Map Services to reconfigurations of the actual resource data stored within Arches.

New map layers can be created with two general definitions, as MapBox layers or tileserver layers, each with its own wide range of options.

For working examples, please see our `arches4-geo-examples <https://github.com/legiongis/arches4-geo-examples>`_ repo.

.. note::
	By default, new map layers are designated as Overlays. To designate the layer as a Basemap, just add ``-b`` to the load commands shown below.

MapBox Layers
`````````````

``python manage.py packages -o add_mapbox_layer -j /path/to/mapbox_style.json -n "New MapBox Layer"``

Arches allows you to make direct references to styles or layers that have been previously defined in `MapBox Studio <https://www.mapbox.com/studio/>`_. You can make entirely new basemap renderings, save them in your MapBox account, then download the style definition and use it here. Read more about `MapBox Styles <https://www.mapbox.com/help/studio-manual-styles/>`_. For more information on commands to create and delete MapBox layers see: :ref:`Creating and Deleting Map Layers`.

Additionally, you can take a MapBox JSON file and place any mapbox.js layer definition in the ``layers`` section, as long as you define its source in the ``sources`` section.

.. note:: One thing to be aware of when trying to cascade a WMS through a MapBox layer is that mapbox.js is `much pickier <https://github.com/mapbox/mapbox-gl-js/issues/2171>`_ about CORS than other js mapping libraries like Leaflet. To use an external WMS or tileset, you may be better off using a tileserver layer as described below. You can find WMS examples in the `arches4-geo-examples <https://github.com/legiongis/arches4-geo-examples>`_ repo.


Making Selectable Vector Layers
-------------------------------

In Arches, it's possible to add a vector layer whose features may be "selectable". This is especially useful during drawing operations. For example, a building footprint dataset could be added as a selectable vector layer, and while creating new building resources you would select and "transfer" these geometries from the overlay to the new Arches resource.

1. First, the data source for the layer may be geojson or vector tiles. This could be a tile server layer serving vector features from PostGIS, for example.
2. Add a property to your vector features called "geojson".
3. Populate this property with either the entire geojson geometry for the feature, or a url that will return a json response containing the entire geojson geometry for the feature. This is necessary to handle the fact that certain geometries may extend across multiple vector tiles.
4. Add the overlay as you would any tileserver layer (see above).

You will now be able to add this layer to the map and select its features by clicking on them.

Adding Click and Hover Styles
-----------------------------

In addition to making overlay features selectable, you can define styles for their hover and click states.

    1. To do so, each feature in your overlay needs a unique `_featureid`. If you're overlay served from PostGIS, you can define this property in the layer config's `queries` array like so::

        "queries": [
            "select gid as __id__, gid as _featureid, site_name, feature_info_content, st_asgeojson(geom) as geojson, st_transform(geom, 900913) as __geometry__ from example_layer"
        ]

    2. Next you will need to ensure your `source-layer` is properly defined. In the source layer the `source-layer` property must match the `id` property and cannot contain spaces or periods. This layer will be hidden when the hover or click layer is revealed, so this should be a fill layer if your click or hover layers contain a fill.

    3. Define the hover and click layers. These each must have a _featureid filter their ids must be suffixed with either a `-click` or `-hover`.  For example::

            {
            "layout": {
                "visibility": "visible"
            },
            "source": "example_layer",
            "filter": [
                "all",
                [
                    "==",
                    "$type",
                    "Polygon"
                ],
                [
                    "==",
                    "_featureid",
                    ""
                ]
            ],
            "paint": {
                "fill-color": "rgb(0, 255, 0)",
                "fill-opacity": 0.5
            },
            "source-layer": "example_layer",
            "type": "fill",
            "id": "example_layer-hover"
        }

    4. If you are loading your layers from a package, each layer must have an accompanying `meta.json` file with a name defined. This will ensure that the `source-layer` property is saved to the layer as you intend. If you do not have a meta.json file, the source-layer name will be the map layer's file name, and will probably not work properly. See the example package for an example:

        https://github.com/archesproject/arches4-example-pkg/tree/master/map_layers/tile_server/overlays/vector_example

Customizing Map Popup Content
-----------------------------

You can display custom HTML in the search map popup when a user hovers or clicks on a feature in a vector layer.

1. First, the data source for the layer may be geojson or vector tiles. This could be a tile server layer serving vector features from PostGIS, for example.
2. Add a property to your vector features called "feature_info_content".
3. Populate this property with either an html element or a url from which to load html. If you use a url, you will need to update the 'ALLOWED_POPUP_HOSTS' to include the host from which you want to request HTML.
4. Add the overlay as you would any tileserver layer (see above).

You will now be able to add this layer to the map see the markup defined in the 'feature_info_content' in the search map popup.