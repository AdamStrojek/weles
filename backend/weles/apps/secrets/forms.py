from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .models import Secret


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
