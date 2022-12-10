from __future__ import unicode_literals, absolute_import

import logging

from django.urls import include, path

from rest_framework_simplejwt.views import TokenRefreshView

from oncourse.apps.apis.views.users.tokens import OnCourseObtainTokenPairView

log = logging.getLogger(__name__)

urlpatterns = [
     path('my/token/', OnCourseObtainTokenPairView.as_view(), name='token_obtain_pair'),
     path('my/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]