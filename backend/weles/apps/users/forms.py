from django_registration.forms import RegistrationForm as BaseRegistrationForm

from .models import User


class RegistrationForm(BaseRegistrationForm):
    class Meta:
        model = User
        fields = [
            User.USERNAME_FIELD,
            User.get_email_field_name(),
            "password1",
            "password2",
        ]
