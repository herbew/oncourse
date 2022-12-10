# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

# from oncourse.apps.masters.serializers.tasks import TaskSerializer

from oncourse.apps.masters.models.answers import Answer

log = logging.getLogger(__name__)

class AnswerSerializer(serializers.ModelSerializer):
    option = serializers.ChoiceField(choices=Answer.TASK_OPTION_CHOICES)
    class Meta:
        model = Answer
        fields = ['id','option', 'detailed']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Answer.objects.all(),
                fields=('task', 'code'),
                message=_("The Answer already exists!")
            )
        ]