from django.contrib.contenttypes.models import ContentType

from .models import Follow


class UserFollowMixin(object):

    def follow(self, item):
        item_type = ContentType.objects.get_for_model(item)
        Follow.objects.create(
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
