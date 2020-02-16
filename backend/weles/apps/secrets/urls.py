from django.urls import path, include

from .views import CreateSecretView, SecretDetailView


urlpatterns = [
    path('add', CreateSecretView.as_view(), name='secret-add'),
    path('<uuid>/', SecretDetailView.as_view(), name='secret-detail'),
]
