class CardModel(models.Model):
    cardid = models.UUIDField(primary_key=True, default=uuid.uuid1)  # This field type is a guess.
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    cssclass = models.TextField(blank=True, null=True)
    helpenabled = models.BooleanField(default=False)
    helptitle = models.TextField(blank=True, null=True)
    helptext = models.TextField(blank=True, null=True)
    nodegroup = models.ForeignKey('NodeGroup', db_column='nodegroupid')
    graph = models.ForeignKey('GraphModel', db_column='graphid')
    active = models.BooleanField(default=True)
    visible = models.BooleanField(default=True)
    sortorder = models.IntegerField(blank=True, null=True, default=None)
    component = models.ForeignKey('CardComponent', db_column='componentid', default=uuid.UUID(
        'f05e4d3a-53c1-11e8-b0ea-784f435179ea'), on_delete=models.SET_DEFAULT)
    config = JSONField(blank=True, null=True, db_column='config')

    def is_editable(self):
        result = True
        tiles = TileModel.objects.filter(nodegroup=self.nodegroup).count()
        result = False if tiles > 0 else True
        if settings.OVERRIDE_RESOURCE_MODEL_LOCK == True:
            result = True
        return result

    class Meta:
        managed = True
        db_table = 'cards'
