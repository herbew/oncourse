# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.masters.models.tasks import Task
from oncourse.apps.masters.models.answers import Answer

from oncourse.apps.masters.serializers.courses import CourseSerializer
from oncourse.apps.masters.serializers.answers import AnswerSerializer


log = logging.getLogger(__name__)

class TaskSerializer(serializers.ModelSerializer):
    course = CourseSerializer(required=True)
    typed = serializers.ChoiceField(choices=Task.TASK_TYPE_CHOICES)
    answers = serializers.SerializerMethodField()
    
    def get_answers(self, obj):
        qs = Answer.objects.filter(task=obj).order_by("option")
        serializer = AnswerSerializer(instance=qs, many=True)
        return serializer.data
    
    class Meta:
        model = Task
        fields = ['id','course', 'name', 'typed', 'detailed', 'answers']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Task.objects.all(),
                fields=('course', 'typed', 'name'),
                message=_("The Task typed of Course already exists!")
            )
        ]