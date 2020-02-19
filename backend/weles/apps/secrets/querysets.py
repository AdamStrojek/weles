from datetime import timedelta

from django.db import models
from django.db.models import Count, Case, When, Q
from django.db.models.functions import TruncDate

from weles.utils import now


class SecretQuerySet(models.QuerySet):
    def active(self, active_date=None):
        """
        Select only active secrets. As active we fetch all Secrets created in last 24h
        :param active_date: alter datetime for which fetch data, if None current date will be used
        :return: queryset of active Secrets
        """
        active_date = active_date or now()
        date_from = active_date - timedelta(days=1)
        return self.filter(created__gte=date_from, created__lte=active_date)


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
