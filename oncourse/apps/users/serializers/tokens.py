# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

log = logging.getLogger(__name__)


class OnCourseTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(OnCourseTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        
        return token