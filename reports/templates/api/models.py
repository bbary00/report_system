from mongoengine import fields, Document
from datetime import datetime


class Template(Document):
    label = fields.StringField()
    description = fields.StringField()
    inputs = fields.ListField(fields.StringField())
    date = fields.DateTimeField(default=datetime.utcnow())

    def __str__(self):
        return self.label


class Report(Document):
    user = fields.DynamicField()
    template = fields.DictField()
    answers = fields.ListField(fields.StringField())
    date = fields.DateTimeField(default=datetime.utcnow())
