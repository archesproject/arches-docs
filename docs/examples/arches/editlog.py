class EditLog(models.Model):
    editlogid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    resourcedisplayname = models.TextField(blank=True, null=True)
    resourceclassid = models.TextField(blank=True, null=True)
    resourceinstanceid = models.TextField(blank=True, null=True)
    nodegroupid = models.TextField(blank=True, null=True)
    tileinstanceid = models.TextField(blank=True, null=True)
    edittype = models.TextField(blank=True, null=True)
    newvalue = JSONField(blank=True, null=True, db_column='newvalue')
    oldvalue = JSONField(blank=True, null=True, db_column='oldvalue')
    newprovisionalvalue = JSONField(blank=True, null=True, db_column='newprovisionalvalue')
    oldprovisionalvalue = JSONField(blank=True, null=True, db_column='oldprovisionalvalue')
    timestamp = models.DateTimeField(blank=True, null=True)
    userid = models.TextField(blank=True, null=True)
    user_firstname = models.TextField(blank=True, null=True)
    user_lastname = models.TextField(blank=True, null=True)
    user_email = models.TextField(blank=True, null=True)
    user_username = models.TextField(blank=True, null=True)
    provisional_userid = models.TextField(blank=True, null=True)
    provisional_user_username = models.TextField(blank=True, null=True)
    provisional_edittype = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'edit_log'
