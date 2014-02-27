from django.contrib.contenttypes.models import ContentType

from .models import Follow


class UserFollowMixin(object):

    def get_follow_set(self, model=None):
        qs = Follow.objects.filter(
            user=self
        ).prefetch_related('target')

        if model:
            model_type = ContentType.objects.get_for_model(model)
            qs = qs.filter(target_content_type=model_type)

        return [x.target for x in qs]

    def follow(self, item):
        item_type = ContentType.objects.get_for_model(item)
        Follow.objects.get_or_create(
            user=self,
            target_content_type=item_type,
            target_object_id=item.pk
        )

    def unfollow(self, item):
        item_type = ContentType.objects.get_for_model(item)
        Follow.objects.filter(
            user=self,
            target_content_type=item_type,
            target_object_id=item.pk
        ).delete()

    def is_following(self, item):
        item_type = ContentType.objects.get_for_model(item)
        return Follow.objects.filter(
            user=self,
            target_content_type=item_type,
            target_object_id=item.pk
        ).exists()


class TargetFollowMixin(object):

    def get_follower_set(self):
        content_type = ContentType.objects.get_for_model(self)
        follows = Follow.objects.filter(
            target_content_type=content_type,
            target_object_id=self.id,
        ).prefetch_related('user')

        return [x.user for x in follows]
