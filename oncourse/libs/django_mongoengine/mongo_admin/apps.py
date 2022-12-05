# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import



from django.apps import AppConfig
from django.core import checks
from django.utils.translation import ugettext_lazy as _

def check_admin_app(**kwargs):
    from oncourse.libs.django_mongoengine.mongo_admin.sites import system_check_errors
    return system_check_errors


class SimpleMongoAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    name = "oncourse.libs.django_mongoengine.mongo_admin"
    verbose_name = _("MongoDB Administration")

    def ready(self):
        checks.register(check_admin_app, checks.Tags.admin)


class MongoAdminConfig(SimpleMongoAdminConfig):

    def ready(self):
        super(MongoAdminConfig, self).ready()
        self.module.autodiscover()
