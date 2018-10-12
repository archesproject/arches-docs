class TileModel(models.Model):  # Tile
    """
    the data JSONField has this schema:

    values are dictionaries with n number of keys that represent nodeid's and values the value of that node instance

    .. code-block:: python

        {
            nodeid: node value,
            nodeid: node value,
            ...
        }

        {
            "20000000-0000-0000-0000-000000000002": "John",
            "20000000-0000-0000-0000-000000000003": "Smith",
            "20000000-0000-0000-0000-000000000004": "Primary"
        }

    the provisionaledits JSONField has this schema:

    values are dictionaries with n number of keys that represent nodeid's and values the value of that node instance

    .. code-block:: python

        {
            userid: {
                value: node value,
                status: "review", "approved", or "rejected"
                action: "create", "update", or "delete"
                reviewer: reviewer's user id,
                timestamp: time of last provisional change,
                reviewtimestamp: time of review
                }
            ...
        }

        {
            1: {
                "value": {
                        "20000000-0000-0000-0000-000000000002": "Jack",
                        "20000000-0000-0000-0000-000000000003": "Smith",
                        "20000000-0000-0000-0000-000000000004": "Primary"
                      },
               "status": "rejected",
                "action": "update",
                "reviewer": 8,
                "timestamp": "20180101T1500",
                "reviewtimestamp": "20180102T0800",
                },
            15: {
                "value": {
                        "20000000-0000-0000-0000-000000000002": "John",
                        "20000000-0000-0000-0000-000000000003": "Smith",
                        "20000000-0000-0000-0000-000000000004": "Secondary"
                      },
                "status": "review",
                "action": "update",
        }

    """

    tileid = models.UUIDField(primary_key=True, default=uuid.uuid1)  # This field type is a guess.
    resourceinstance = models.ForeignKey(ResourceInstance, db_column='resourceinstanceid')
    parenttile = models.ForeignKey('self', db_column='parenttileid', blank=True, null=True)
    data = JSONField(blank=True, null=True, db_column='tiledata')  # This field type is a guess.
    nodegroup = models.ForeignKey(NodeGroup, db_column='nodegroupid')
    sortorder = models.IntegerField(blank=True, null=True, default=0)
    provisionaledits = JSONField(blank=True, null=True, db_column='provisionaledits')  # This field type is a guess.

    class Meta:
        managed = True
        db_table = 'tiles'

    def save(self, *args, **kwargs):
        if(self.sortorder is None or (self.provisionaledits is not None and self.data == {})):
            sortorder_max = TileModel.objects.filter(
                nodegroup_id=self.nodegroup_id, resourceinstance_id=self.resourceinstance_id).aggregate(Max('sortorder'))['sortorder__max']
            self.sortorder = sortorder_max + 1 if sortorder_max is not None else 0
        super(TileModel, self).save(*args, **kwargs)  # Call the "real" save() method.
