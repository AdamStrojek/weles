import factory

from .models import Secret, SecretAccessLog
from ..users.factories import UserFactory


class SecretFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Secret

    user = factory.SubFactory(UserFactory)
    title = factory.Sequence(lambda n: f"secret_{n}")
    password = ""
    url = factory.Sequence(lambda n: f"https://weles.herokuapp.com/{n}")


class SecretFileFactory(SecretFactory):
    file = factory.django.FileField(filename='secret_file.png')


# class SecretURLFactory(SecretFactory):


class SecretAccessLogFactory(factory.Factory):
    class Meta:
        model = SecretAccessLog

