# -*- coding: utf-8 -*-
from django.apps import AppConfig


class ModeltranslationConfig(AppConfig):
    name = 'oncourse.libs.modeltranslation'
    verbose_name = 'Modeltranslation'

    def ready(self):
        from oncourse.libs.modeltranslation.models import handle_translation_registrations
        handle_translation_registrations()
