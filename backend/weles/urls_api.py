from django.urls import include, path


urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('', include('weles.apps.secrets.api.urls')),
]
