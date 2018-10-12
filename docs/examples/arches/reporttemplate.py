class ReportTemplate(models.Model):
    templateid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    name = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    component = models.TextField()
    componentname = models.TextField()
    defaultconfig = JSONField(blank=True, null=True, db_column='defaultconfig')

    @property
    def defaultconfig_json(self):
        json_string = json.dumps(self.defaultconfig)
        return json_string

    class Meta:
        managed = True
        db_table = 'report_templates'
