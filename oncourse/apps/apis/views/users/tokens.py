from __future__ import unicode_literals, absolute_import

import logging

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

log = logging.getLogger(__name__)

from oncourse.apps.users.serializers.tokens import (
    OnCourseTokenObtainPairSerializer)

log = logging.getLogger(__name__)

class OnCourseObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = OnCourseTokenObtainPairSerializer