class OntologyClass(models.Model):
    """
    the target JSONField has this schema:

    values are dictionaries with 2 properties, 'down' and 'up' and within each of those another 2 properties,
    'ontology_property' and 'ontology_classes'

    "down" assumes a known domain class, while "up" assumes a known range class

    .. code-block:: python

        "down":[
            {
                "ontology_property": "P1_is_identified_by",
                "ontology_classes": [
                    "E51_Contact_Point",
                    "E75_Conceptual_Object_Appellation",
                    "E42_Identifier",
                    "E45_Address",
                    "E41_Appellation",
                    ....
                ]
            }
        ]
        "up":[
                "ontology_property": "P1i_identifies",
                "ontology_classes": [
                    "E51_Contact_Point",
                    "E75_Conceptual_Object_Appellation",
                    "E42_Identifier"
                    ....
                ]
            }
        ]

    """

    ontologyclassid = models.UUIDField(default=uuid.uuid1, primary_key=True)
    source = models.TextField()
    target = JSONField(null=True)
    ontology = models.ForeignKey('Ontology', db_column='ontologyid', related_name='ontologyclasses')

    class Meta:
        managed = True
        db_table = 'ontologyclasses'
        unique_together = (('source', 'ontology'),)
