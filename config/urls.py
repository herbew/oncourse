from __future__ import unicode_literals, absolute_import

from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.urls import include, path

from django.contrib import admin
from django.conf.urls.static import static

from django.views import defaults as default_views
from django.views.generic import TemplateView

from rest_framework_swagger.views import get_swagger_view

from oncourse.apps.users.views import signup, signin
from allauth.account.views import password_change


schema_url_patterns = [path('api/', include('oncourse.apps.apis.urls', namespace='api')),]
swagger_schema_view = get_swagger_view(title='Crawler API',
                                       patterns=schema_url_patterns)


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    
]


urlpatterns += i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("accounts/", include("allauth.urls")),
    path("accounts/signup/",signup.signup, name='signup'),
    path("accounts/signup/None/", 
        TemplateView.as_view(template_name='pages/home.html')),
    path("accounts/profile/", signin.signup_redirect, name='signup_redirect' ),
    path("accounts/login/None/", 
        signin.redirect, name='redirect'),
         
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("settings/password/change/", 
        password_change, 
        name='setting_change_password'),
    path("logout/", TemplateView.as_view(template_name='account/logout.html'), 
        name="logout"),
    
    # oauth2_provider
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    
    path("avatar/", 
        include("oncourse.libs.avatar.urls", namespace="avatar"),
        ),
    path("messages/", 
         include("oncourse.libs.django_messages.urls", namespace="messages")),
    
    # Django Social oauth2
    path("auth/", include('rest_framework_social_oauth2.urls')),
    
    
    
    # User Management
    path("trails/", include('oncourse.apps.trails.urls', 
                    namespace='trails')),
    # path("users/", include('oncourse.apps.users.urls', 
    #                 namespace='users')),
    
    # path("masters/", include('oncourse.apps.masters.urls', 
    #                 namespace='masters')),
    
    # path("api/", include('oncourse.apps.apis.urls', 
    #                 namespace='api')),
    
    path("api-auth/", include('rest_framework.urls',
                       namespace='rest_framework')),
    
    path('api/', swagger_schema_view),
    path("api/", include('oncourse.apps.apis.urls', 
                     namespace='api')),

) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
