from __future__ import unicode_literals, absolute_import

import logging
import os

from django_mongoengine import mongo_admin 

log = logging.getLogger(__name__)

from oncourse.apps.trails.models.files import MetaFile
from oncourse.apps.trails.models.summernotes import MetaSummernote

@mongo_admin.register(MetaFile)
class MetaFileAdmin(mongo_admin.DocumentAdmin):
    pass

@mongo_admin.register(MetaSummernote)
class MetaSummernoteAdmin(mongo_admin.DocumentAdmin):
    pass
