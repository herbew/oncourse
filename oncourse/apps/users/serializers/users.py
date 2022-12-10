# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import serializers

from oncourse.apps.users.models.users import User

log = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name', 'email']