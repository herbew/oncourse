# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from oncourse.apps.academics.models.events import Event, StudentEvent

from oncourse.apps.masters.serializers.courses import CourseSerializer
from oncourse.apps.workbooks.serializers.users import UserTraceabilitySerializer

log = logging.getLogger(__name__)

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Event
        fields = ['name', 'date_event', 'start_ts', 'end_ts']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Event.objects.all(),
                fields=('name', 'date_event'),
                message=_("The Event already exists!")
            )
        ]

        
class StudentEventSerializer(serializers.ModelSerializer):
    event = EventSerializer(required=True)
    course = CourseSerializer(required=True)
    user_traceability = UserTraceabilitySerializer(required=True)
    
    class Meta:
        model = StudentEvent
        fields = ['event', 'course', 'user_traceability']
        
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=StudentEvent.objects.all(),
                fields=('event', 'course', 'user_traceability'),
                message=_("The Student, Course of event already exists!")
            )
        ]