from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .managers import FollowManager


class Follow(models.Model):
    user = models.ForeignKey(getattr(settings, 'AUTH_USER_MODEL', 'auth.User'))
    created = models.DateTimeField(auto_now_add=True)

    # generic foreign key to target
    target_content_type = models.ForeignKey(ContentType)
    target_object_id = models.PositiveIntegerField()
    target = generic.GenericForeignKey('target_content_type', 'target_object_id')

    objects = FollowManager()

    class Meta:
        unique_together = ('user', 'target_content_type', 'target_object_id')


# apply user model mixins to auth.User model
if getattr(settings, 'AUTH_USER_MODEL', 'auth.User') == 'auth.User':
    from .model_mixins import UserFollowMixin
    from django.contrib.auth.models import User

    for name, method in UserFollowMixin.__dict__.items():
        if not name.startswith('__'):
            User.add_to_class(name, method)
