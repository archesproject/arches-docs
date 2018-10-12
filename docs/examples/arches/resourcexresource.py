class ResourceXResource(models.Model):
    resourcexid = models.UUIDField(primary_key=True, default=uuid.uuid1)  # This field type is a guess.
    resourceinstanceidfrom = models.ForeignKey(
        'ResourceInstance', db_column='resourceinstanceidfrom', blank=True, null=True, related_name='resxres_resource_instance_ids_from')
    resourceinstanceidto = models.ForeignKey(
        'ResourceInstance', db_column='resourceinstanceidto', blank=True, null=True, related_name='resxres_resource_instance_ids_to')
    notes = models.TextField(blank=True, null=True)
    relationshiptype = models.TextField(blank=True, null=True)
    datestarted = models.DateField(blank=True, null=True)
    dateended = models.DateField(blank=True, null=True)
    created = models.DateTimeField()
    modified = models.DateTimeField()

    def delete(self):
        from arches.app.search.search_engine_factory import SearchEngineFactory
        se = SearchEngineFactory().create()
        se.delete(index='resource_relations', doc_type='all', id=self.resourcexid)
        super(ResourceXResource, self).delete()

    def save(self):
        from arches.app.search.search_engine_factory import SearchEngineFactory
        se = SearchEngineFactory().create()
        if not self.created:
            self.created = datetime.datetime.now()
        self.modified = datetime.datetime.now()
        document = model_to_dict(self)
        se.index_data(index='resource_relations', doc_type='all', body=document, idfield='resourcexid')
        super(ResourceXResource, self).save()

    class Meta:
        managed = True
        db_table = 'resource_x_resource'
