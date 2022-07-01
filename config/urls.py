from django.conf import settings
from django.urls import include, path ,re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from ipad_config import views
import nested_admin

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


urlpatterns = [
    path("", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("shortcuts/", views.shortcuts, name="shortcuts"),
    path("admin/statuscheck/", include('celerybeat_status.urls')),
    path(
        "about/", TemplateView.as_view(template_name="pages/trash/about.html"), name="about"
    ),

    # Django Admin, use {% url 'admin:index' %}
    path('^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path(settings.ADMIN_URL, admin.site.urls),
    path('^nested_admin/', include('nested_admin.urls')),

    # User management
    path("users/", include("setup.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("api/main_features/<int:pk>/", views.MainFeatureUpdate.as_view()),

    #token generation and verification
    path('api/token/v1/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/v1/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/v1/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/create_user/', views.CreateActiveUser.as_view(), name='create_user'),

    # path("dv5/", views.dv5_head_response),
    path("api/main_features/profile/<int:profile>/", views.MainFeatureList.as_view()),
    re_path(r'^dv5/(?P<file_path>.*.sqlite)$', views.media_content, name="export_sqlite"),

    # Your stuff: custom urls includes go here
    path("oauth/", include('oauth2_provider.urls', namespace='oauth2_provider')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("hotels/", include("ipad_config.urls")),
    path("themes/", include("ipad_config.themes_url")),
    path("language/", include("ipad_config.language_url")),
]


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
