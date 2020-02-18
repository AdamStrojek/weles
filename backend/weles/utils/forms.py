from django.contrib.auth.hashers import make_password
from django.forms import CharField, PasswordInput


class PasswordField(CharField):
    widget = PasswordInput()

    def to_python(self, value):
        internal_value = super(PasswordField, self).to_python(value)
        internal_value = make_password(internal_value)
        return internal_value
