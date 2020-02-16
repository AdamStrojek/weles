from django.contrib import admin

from .models import Secret
from .forms import AdminSecretForm


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    form = AdminSecretForm

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False
