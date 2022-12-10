# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import serializers

from oncourse.apps.masters.models.courses import Course


log = logging.getLogger(__name__)

class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'order_no']
        