from __future__ import unicode_literals, absolute_import

import logging

from rest_framework import routers
from django.urls import include, path

from oncourse.apps.masters.views.hellos import ApiHello

log = logging.getLogger(__name__)

router = routers.DefaultRouter()

router.register(r'hello', ApiHello, basename="apihello")

urlpatterns = [
    path(r"", include(router.urls)),
    path("api-auth/", include('rest_framework.urls',
                       namespace='rest_framework')),
]
