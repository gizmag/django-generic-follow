from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model


class FollowQuerySet(QuerySet):
    pass


class FollowManager(models.Manager):
    def get_queryset(self):
        return FollowQuerySet(self.model)

    def __getattr__(self, attr, *args):
        if attr.startswith("_"):
            raise AttributeError
        return getattr(self.get_queryset(), attr, *args)

    def create_batch(self, users, target):
        target_content_type = ContentType.objects.get_for_model(target)
        Follow = get_model('generic_follow', 'Follow')
        follows = list()
        for user in users:
            list.append(
                Follow(
                    user=user,
                    target_content_type=target_content_type,
                    target_id=target.pk
                )
            )
        self.objects.bulk_create(follows)
