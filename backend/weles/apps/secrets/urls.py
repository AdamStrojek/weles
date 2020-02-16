from django.urls import path, include

from .views import CreateSecretView, SecretDetailView, SecretAccessLogView


urlpatterns = [
    path('add/', CreateSecretView.as_view(), name='secret-add'),
    path('stats/', SecretAccessLogView.as_view(), name='secret-stats'),
    path('<uuid>/', SecretDetailView.as_view(), name='secret-detail'),
]
