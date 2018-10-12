class Ontology(models.Model):
    ontologyid = models.UUIDField(default=uuid.uuid1, primary_key=True)
    name = models.TextField()
    version = models.TextField()
    path = models.FileField(storage=get_ontology_storage_system())
    parentontology = models.ForeignKey('Ontology', db_column='parentontologyid',
                                       related_name='extensions', null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'ontologies'
