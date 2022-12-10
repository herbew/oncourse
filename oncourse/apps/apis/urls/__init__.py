# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from oncourse.apps.apis.urls.hellos import urlpatterns as hellos_urlpatterns
from oncourse.apps.apis.urls.users.tokens import (
    urlpatterns as users_tokens_urlpatterns)

from oncourse.apps.apis.urls.academics.events import (
    urlpatterns as academics_events_urlpatterns
    )

app_name = "apis"

urlpatterns = hellos_urlpatterns
urlpatterns += users_tokens_urlpatterns
urlpatterns += academics_events_urlpatterns