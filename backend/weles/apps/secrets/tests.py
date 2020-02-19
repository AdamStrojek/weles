from datetime import datetime, timedelta

from django.test import TestCase

from .factories import SecretFactory
from .models import Secret


class SecretTestCase(TestCase):
    def setUp(self) -> None:
        self.now = datetime.utcnow()
        self.secrets = SecretFactory.create_batch(24)

        for i, secret in enumerate(self.secrets):
            secret.created += timedelta(hours=i)
            secret.save()

    def test_all_available_secrets(self):
        self.assertEqual(Secret.objects.all().count(), 24)

    def test_all_secrets_using_now(self):
        self.assertEqual(Secret.objects.active(self.now).count(), 0)

    def test_all_secrets_in_12h(self):
        self.assertEqual(Secret.objects.active(self.now + timedelta(hours=12)).count(), 12)

    def test_all_secrets_in_24h(self):
        self.assertEqual(Secret.objects.active(self.now + timedelta(hours=24)).count(), 24)

    def test_all_secrets_in_25h(self):
        self.assertEqual(Secret.objects.active(self.now + timedelta(hours=25)).count(), 23)

    def test_all_secrets_in_26h(self):
        self.assertEqual(Secret.objects.active(self.now + timedelta(hours=26)).count(), 22)

    def test_all_secrets_in_27h(self):
        self.assertEqual(Secret.objects.active(self.now + timedelta(hours=27)).count(), 21)

    def test_all_secrets_in_48h(self):
        self.assertEqual(Secret.objects.active(self.now + timedelta(hours=48)).count(), 0)
