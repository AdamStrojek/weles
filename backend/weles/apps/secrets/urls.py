from django.urls import path, include

from .views import SecretCreateView, SecretDetailView, SecretAccessLogView


urlpatterns = [
    path('add/', SecretCreateView.as_view(), name='secrets-create'),
    path('stats/', SecretAccessLogView.as_view(), name='secrets-stats'),
    path('<uuid>/', SecretDetailView.as_view(), name='secrets-detail'),
]
