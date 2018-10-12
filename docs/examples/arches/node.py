class Node(models.Model):
    """
    Name is unique across all resources because it ties a node to values within tiles. Recommend prepending resource class to node name.

    """

    nodeid = models.UUIDField(primary_key=True, default=uuid.uuid1)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    istopnode = models.BooleanField()
    ontologyclass = models.TextField(blank=True, null=True)
    datatype = models.TextField()
    nodegroup = models.ForeignKey(NodeGroup, db_column='nodegroupid', blank=True, null=True)
    graph = models.ForeignKey(GraphModel, db_column='graphid', blank=True, null=True)
    config = JSONField(blank=True, null=True, db_column='config')
    issearchable = models.BooleanField(default=True)
    isrequired = models.BooleanField(default=False)
    sortorder = models.IntegerField(blank=True, null=True, default=0)

    def get_child_nodes_and_edges(self):
        """
        gather up the child nodes and edges of this node

        returns a tuple of nodes and edges

        """
        nodes = []
        edges = []
        for edge in Edge.objects.filter(domainnode=self):
            nodes.append(edge.rangenode)
            edges.append(edge)

            child_nodes, child_edges = edge.rangenode.get_child_nodes_and_edges()
            nodes.extend(child_nodes)
            edges.extend(child_edges)
        return (nodes, edges)

    @property
    def is_collector(self):
        return str(self.nodeid) == str(self.nodegroup_id) and self.nodegroup is not None

    def get_relatable_resources(self):
        relatable_resource_ids = [
            r2r.resourceclassfrom for r2r in Resource2ResourceConstraint.objects.filter(resourceclassto_id=self.nodeid)]
        relatable_resource_ids = relatable_resource_ids + \
            [r2r.resourceclassto for r2r in Resource2ResourceConstraint.objects.filter(
                resourceclassfrom_id=self.nodeid)]
        return relatable_resource_ids

    def set_relatable_resources(self, new_ids):
        old_ids = [res.nodeid for res in self.get_relatable_resources()]
        for old_id in old_ids:
            if old_id not in new_ids:
                Resource2ResourceConstraint.objects.filter(Q(resourceclassto_id=self.nodeid) | Q(
                    resourceclassfrom_id=self.nodeid), Q(resourceclassto_id=old_id) | Q(resourceclassfrom_id=old_id)).delete()
        for new_id in new_ids:
            if new_id not in old_ids:
                new_r2r = Resource2ResourceConstraint.objects.create(
                    resourceclassfrom_id=self.nodeid, resourceclassto_id=new_id)
                new_r2r.save()

    class Meta:
        managed = True
        db_table = 'nodes'
