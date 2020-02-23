from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth.admin import sensitive_post_parameters_m
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import escape

from .models import Secret
from .forms import AdminSecretForm, AdminSecretPasswordForm


@admin.register(Secret)
class SecretAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'title', 'created']
    form = AdminSecretForm
    change_password_form = AdminSecretPasswordForm
    change_user_password_template = None

    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    @sensitive_post_parameters_m
    def user_change_password(self, request, id, form_url=''):
        secret_obj = self.get_object(request, unquote(id))
        if not self.has_change_permission(request, secret_obj):
            raise PermissionDenied
        if secret_obj is None:
            raise Http404('%(name)s object with primary key %(key)r does not exist.' % {
                'name': self.model._meta.verbose_name,
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(secret_obj, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, secret_obj, change_message)
                msg = 'Password changed successfully.'
                messages.success(request, msg)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            secret_obj._meta.app_label,
                            secret_obj._meta.model_name,
                        ),
                        args=(secret_obj.pk,),
                    )
                )
        else:
            form = self.change_password_form(secret_obj)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': 'Change password: %s' % str(secret_obj),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': secret_obj,
            'save_as': False,
            'show_save': True,
            **self.admin_site.each_context(request),
        }

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/secrets/change_password.html',
            context,
        )
