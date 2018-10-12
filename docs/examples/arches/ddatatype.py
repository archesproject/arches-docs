class DDataType(models.Model):
    datatype = models.TextField(primary_key=True)
    iconclass = models.TextField()
    modulename = models.TextField(blank=True, null=True)
    classname = models.TextField(blank=True, null=True)
    defaultwidget = models.ForeignKey(db_column='defaultwidget', to='models.Widget', null=True)
    defaultconfig = JSONField(blank=True, null=True, db_column='defaultconfig')
    configcomponent = models.TextField(blank=True, null=True)
    configname = models.TextField(blank=True, null=True)
    issearchable = models.NullBooleanField(default=False)
    isgeometric = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'd_data_types'
