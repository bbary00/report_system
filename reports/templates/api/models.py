# from mongoengine import Document, EmbeddedDocument, fields
from djongo import models

class ToolInput(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    objects = models.DjongoManager()

    def __str__(self):
        return str(self.name)


class Tool(models.Model):
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True)
    inputs = models.ListField(models.EmbeddedModelField(
                                        model_container=ToolInput))
    objects = models.DjongoManager()

    def __str__(self):
        return str(self.label)
