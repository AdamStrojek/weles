from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password, is_password_usable
from django.db import models
from django.urls import reverse

from .querysets import SecretQuerySet, SecretAccessLogQuerySet

User = get_user_model()


class Secret(models.Model):
    uuid = models.UUIDField(default=uuid4)
    user = models.ForeignKey(User, models.CASCADE)
    title = models.CharField('title', max_length=255)
    password = models.CharField('password', max_length=128)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    file = models.FileField(blank=True)
    url = models.URLField(blank=True)

    objects = SecretQuerySet.as_manager()

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def __str__(self):
        return self.title

    def get_web_url(self):
        return reverse('secrets-access', kwargs={'uuid': self.uuid})

    def get_redirect(self):
        if self.url:
            return self.url
        return self.file.url

    def create_access_log(self, request):
        return SecretAccessLog.objects.create(
            secret=self,
            user_agent=request.META.get('HTTP_USER_AGENT', 'unknown'),
        )


class SecretAccessLog(models.Model):
    secret = models.ForeignKey(Secret, models.CASCADE, related_name='log')
    user_agent = models.TextField()  # Text field, because some browsers are generating a lot of text
    created = models.DateTimeField(auto_now_add=True)

    objects = SecretAccessLogQuerySet.as_manager()
