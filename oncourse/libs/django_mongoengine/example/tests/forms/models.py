from django.db import models
from oncourse.libs.django_mongoengine import fields, Document

class MongoDoc(Document):
    intfield = fields.IntField()


class DjangoModel(models.Model):
    intfield = models.IntegerField()
