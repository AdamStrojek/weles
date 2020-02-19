from django.urls import include, path

from .resources import SecretAccessLogAPIView, SecretCreateAPIView, SecretRetrieveAPIView, SecretAccessAPIView

urlpatterns = [
    path('', SecretCreateAPIView.as_view(), name='api-secrets-create'),
    path('stats/', SecretAccessLogAPIView.as_view(), name='api-secrets-log'),
    path('<uuid>/', SecretRetrieveAPIView.as_view(), name='api-secrets-retrieve'),
    path('<uuid>/access/', SecretAccessAPIView.as_view(), name='api-secrets-access'),
]
