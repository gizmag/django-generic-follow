from django.db import models
from django.db.models.query import QuerySet


class FollowQuerySet(QuerySet):
    pass


class FollowManager(models.Manager):
    def get_queryset(self):
        return FollowQuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_queryset(), attr, *args)
