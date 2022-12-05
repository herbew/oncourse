# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from oncourse.libs.django_mongoengine.document import Document, DynamicDocument, EmbeddedDocument, DynamicEmbeddedDocument
from oncourse.libs.django_mongoengine.queryset import QuerySet, QuerySetNoCache

__all__ = ["QuerySet", "QuerySetNoCache", "Document", "DynamicDocument", "EmbeddedDocument", "DynamicEmbeddedDocument"]

default_app_config = 'oncourse.libs.django_mongoengine.apps.DjangoMongoEngineConfig'
