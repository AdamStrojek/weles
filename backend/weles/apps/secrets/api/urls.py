from rest_framework.routers import DefaultRouter

from .resources import SecretViewSet, SecretAccessLogViewSet


router = DefaultRouter()
router.register(r'secrets', SecretViewSet, basename='api-secrets')
router.register(r'stats', SecretAccessLogViewSet, basename='api-stats')
urlpatterns = router.urls
