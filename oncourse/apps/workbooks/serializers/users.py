# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.users.serializers.users import UserSerializer

from oncourse.apps.workbooks.models.users import UserTraceability


log = logging.getLogger(__name__)

class UserTraceabilitySerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    typed = serializers.ChoiceField(choices=UserTraceability.USER_CHOICES)
    class Meta:
        model = UserTraceability
        fields = ['user', 'typed']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=UserTraceability.objects.all(),
                fields=('user', 'typed'),
                message=_("User typed already exists!")
            )
        ]