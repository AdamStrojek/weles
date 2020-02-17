import datetime

from django.db import models
from django.db.models import Count, Case, When, Q
from django.db.models.functions import TruncDate


class SecretQuerySet(models.QuerySet):
    def active(self):
        """
        Select only active secrets. As active we fetch all Secrets created in last 24h
        :return: queryset of active Secrets
        """
        date_from = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        return self.filter(created__gte=date_from)


class SecretAccessLogQuerySet(models.QuerySet):
    def statistics(self):
        return self.select_related('secret') \
            .annotate(date=TruncDate('created')) \
            .values('date') \
            .annotate(
                files=Count(Case(When(secret__url__exact="", then=1),),),
                urls=Count(Case(When(~Q(secret__url__exact=""), then=1),),)
            ) \
            .values('date', 'files', 'urls')
