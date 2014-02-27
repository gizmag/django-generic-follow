from django.db import models
from generic_follow.model_mixins import TargetFollowMixin


class Band(TargetFollowMixin, models.Model):
    name = models.CharField(max_length=255)


class Photographer(TargetFollowMixin, models.Model):
    name = models.CharField(max_length=255)
