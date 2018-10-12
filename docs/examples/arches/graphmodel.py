class GraphModel(models.Model):
    graphid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deploymentfile = models.TextField(blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    deploymentdate = models.DateTimeField(blank=True, null=True)
    version = models.TextField(blank=True, null=True)
    isresource = models.BooleanField()
    isactive = models.BooleanField()
    iconclass = models.TextField(blank=True, null=True)
    color = models.TextField(blank=True, null=True)
    subtitle = models.TextField(blank=True, null=True)
    ontology = models.ForeignKey('Ontology', db_column='ontologyid', related_name='graphs', null=True, blank=True)
    functions = models.ManyToManyField(to='Function', through='FunctionXGraph')
    jsonldcontext = models.TextField(blank=True, null=True)
    template = models.ForeignKey(
        'ReportTemplate',
        db_column='templateid',
        default='50000000-0000-0000-0000-000000000001'
    )
    config = JSONField(db_column='config', default={})

    @property
    def disable_instance_creation(self):
        if not self.isresource:
            return _('Only resource models may be edited - branches are not editable')
        if not self.isactive:
            return _('Set resource model status to Active in Graph Designer')
        return False

    def is_editable(self):
        result = True
        if self.isresource:
            resource_instances = ResourceInstance.objects.filter(graph_id=self.graphid).count()
            result = False if resource_instances > 0 else True
            if settings.OVERRIDE_RESOURCE_MODEL_LOCK == True:
                result = True
        return result

    class Meta:
        managed = True
        db_table = 'graphs'
