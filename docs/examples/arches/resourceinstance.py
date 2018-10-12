class ResourceInstance(models.Model):
    resourceinstanceid = models.UUIDField(primary_key=True, default=uuid.uuid1)  # This field type is a guess.
    graph = models.ForeignKey(GraphModel, db_column='graphid')
    legacyid = models.TextField(blank=True, unique=True, null=True)
    createdtime = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'resource_instances'
