# -*- coding: utf-8 -*-
from django.db.models import F, Q
from django.core.management.base import BaseCommand

from oncourse.libs.modeltranslation.settings import DEFAULT_LANGUAGE
from oncourse.libs.modeltranslation.translator import translator
from oncourse.libs.modeltranslation.utils import build_localized_fieldname


class Command(BaseCommand):
    help = ('Updates empty values of default translation fields using'
            ' values from original fields (in all translated models).')

    def add_arguments(self, parser):
        parser.add_argument(
            'app_label', nargs='?',
            help='App label of an application to update empty values.',
        )
        parser.add_argument(
            'model_name', nargs='?',
            help='Model name to update empty values of only this model.',
        )

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        if verbosity > 0:
            self.stdout.write("Using default language: %s" % DEFAULT_LANGUAGE)

        # get all models excluding proxy- and not managed models
        models = translator.get_registered_models(abstract=False)
        models = [m for m in models if not m._meta.proxy and m._meta.managed]

        # optionally filter by given app_label
        app_label = options['app_label']
        if app_label:
            models = [m for m in models if m._meta.app_label == app_label]

        # optionally filter by given model_name
        model_name = options['model_name']
        if model_name:
            model_name = model_name.lower()
            models = [m for m in models if m._meta.model_name == model_name]

        if verbosity > 0:
            self.stdout.write("Working on models: %s" % ', '.join([
                "{app_label}.{object_name}".format(**m._meta.__dict__)
                for m in models
            ]))

        for model in models:
            if verbosity > 0:
                self.stdout.write("Updating data of model '%s'" % model)

            opts = translator.get_options_for_model(model)
            for field_name in opts.fields.keys():
                def_lang_fieldname = build_localized_fieldname(field_name, DEFAULT_LANGUAGE)

                # We'll only update fields which do not have an existing value
                q = Q(**{def_lang_fieldname: None})
                field = model._meta.get_field(field_name)
                if field.empty_strings_allowed:
                    q |= Q(**{def_lang_fieldname: ""})

                model._default_manager.filter(q).rewrite(False).update(
                    **{def_lang_fieldname: F(field_name)}
                )
