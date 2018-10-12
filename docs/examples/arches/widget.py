class Widget(models.Model):
    widgetid = models.UUIDField(primary_key=True, default=uuid.uuid1)  # This field type is a guess.
    name = models.TextField(unique=True)
    component = models.TextField(unique=True)
    defaultconfig = JSONField(blank=True, null=True, db_column='defaultconfig')
    helptext = models.TextField(blank=True, null=True)
    datatype = models.TextField()

    @property
    def defaultconfig_json(self):
        json_string = json.dumps(self.defaultconfig)
        return json_string

    class Meta:
        managed = True
        db_table = 'widgets'
