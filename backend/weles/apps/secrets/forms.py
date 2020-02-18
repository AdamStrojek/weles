from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import widgets

from .models import Secret
from ...utils.forms import PasswordField
from ...utils.validators import url_or_file_validator


class AdminSecretForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text='Raw passwords are not stored, so there is no way to see this '
                  'user’s password, but you can change the password using '
                  '<a href="{}">this form</a>.'
    )

    class Meta:
        model = Secret
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')


class AdminSecretPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': 'The two password fields didn’t match.',
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )

    def __init__(self, secret_obj, *args, **kwargs):
        self.user = secret_obj
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.secret_obj.set_password(password)
        if commit:
            self.secret_obj.save()
        return self.secret_obj


class AddSecretForm(forms.ModelForm):
    password = PasswordField()

    class Meta:
        model = Secret
        fields = ['title', 'password', 'file', 'url']

    def clean(self):
        cleaned_data = super().clean()

        result = url_or_file_validator(cleaned_data)

        if result is not None:
            raise ValidationError(result)

        return cleaned_data


class CheckPasswordSecretForm(forms.Form):
    password = forms.CharField(widget=widgets.PasswordInput())

    def __init__(self, secret_obj=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_obj = secret_obj

    def clean_password(self):
        raw_password = self.cleaned_data['password']
        if not self.secret_obj.check_password(raw_password):
            raise ValidationError("Password do not match!")

        return raw_password
