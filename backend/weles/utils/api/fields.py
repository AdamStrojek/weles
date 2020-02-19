from django.contrib.auth.hashers import make_password
from rest_framework.fields import URLField
from rest_framework.serializers import CharField


class PasswordField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['write_only'] = True
        super(PasswordField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        value = super(PasswordField, self).to_internal_value(data)
        value = make_password(value)
        return value


class AbsoluteURLField(URLField):
    def to_representation(self, value):
        result = super(AbsoluteURLField, self).to_representation(value)

        if 'request' in self.context:
            result = self.context['request'].build_absolute_uri(result)

        return result
