from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from weles.utils.api.fields import PasswordField, AbsoluteURLField
from weles.utils.validators import url_or_file_validator
from ..models import Secret


def url_or_file_serializer_validator(attrs, serializer=None):
    error = url_or_file_validator(attrs)

    if error is not None:
        raise ValidationError(error)


class SecretSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(read_only=True)
    password = PasswordField(required=True)
    file = serializers.FileField(required=False)
    url = serializers.URLField(required=False)

    secret_web_access_url = AbsoluteURLField(source='get_web_url', read_only=True)
    secret_api_access_url = AbsoluteURLField(source='get_api_url', read_only=True)

    class Meta:
        model = Secret
        fields = ['uuid', 'title', 'password', 'file', 'url', 'secret_web_access_url', 'secret_api_access_url']

        validators = [url_or_file_serializer_validator]


class PasswordValidator:
    requires_context = True

    def __call__(self, value, serializer_field):
        context = serializer_field.context
        if 'instance' not in context:
            raise ValidationError("Unexpected behaviour occured")

        instance: Secret = context['instance']

        if not instance.check_password(value):
            raise ValidationError("Password do not match")


class SecretPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, validators=[PasswordValidator()])

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
