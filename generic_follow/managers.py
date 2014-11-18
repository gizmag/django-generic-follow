from django.db import models
from django.db.models.query import QuerySet
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model
from .signals import follow_bulk_create, follow_bulk_delete


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
            follows.append(
                Follow(
                    user=user,
                    target_content_type=target_content_type,
                    target_object_id=target.pk
                )
            )
        self.bulk_create(follows)
        follow_bulk_create.send(sender=self.model, users=users, target=target)

    def delete_batch(self, users, target):
        target_content_type = ContentType.objects.get_for_model(target)

        self.filter(
            user__in=users,
            target_content_type=target_content_type,
            target_object_id=target.pk,
        ).delete()
        follow_bulk_delete.send(sender=self.model, users=users, target=target)

    def update_batch(self, users_follow, target):
        Follow = get_model('generic_follow', 'Follow')
        target_content_type = ContentType.objects.get_for_model(target)
        existing_follows = Follow.objects.filter(
            target_content_type=target_content_type,
            target_object_id=target.pk
        ).values_list(
            'user__pk',
            flat=True
        )
        pending_create_users = list()
        pending_delete_users = list()
        for user, follow in users_follow:
            if follow and user.pk not in existing_follows:
                pending_create_users.append(user)
            elif not follow and user.pk in existing_follows:
                pending_delete_users.append(user)
        self.delete_batch(pending_delete_users, target)
        self.create_batch(pending_create_users, target)
