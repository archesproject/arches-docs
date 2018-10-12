class NodeGroup(models.Model):
    nodegroupid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    legacygroupid = models.TextField(blank=True, null=True)
    cardinality = models.TextField(blank=True, default='1')
    parentnodegroup = models.ForeignKey('self', db_column='parentnodegroupid',
                                        blank=True, null=True)  # Allows nodegroups within nodegroups

    class Meta:
        managed = True
        db_table = 'node_groups'

        default_permissions = ()
        permissions = (
            ('read_nodegroup', 'Read'),
            ('write_nodegroup', 'Create/Update'),
            ('delete_nodegroup', 'Delete'),
            ('no_access_to_nodegroup', 'No Access'),
        )
