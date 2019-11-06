from mongoengine import Document, EmbeddedDocument, fields, DynamicDocument


class ToolInput(EmbeddedDocument):
    name = fields.StringField()
    value = fields.DynamicField()

    class Meta:
        abstract = True


class Tool(DynamicDocument):
    label = fields.StringField()
    description = fields.StringField()
    inputs = fields.ListField(fields.EmbeddedDocumentField(ToolInput))

    def __str__(self):
        return self.label

