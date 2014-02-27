from django.test import TestCase
from django.contrib.auth.models import User
from generic_follow.models import Follow
from .models import Band


class GenericFollowModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            password='password'
        )
        self.band = Band.objects.create(name='Foals')

    def test_user_can_follow_band(self):
        self.user.follow(self.band)

        follow = Follow.objects.all()[0]

        self.assertEqual(follow.user, self.user)
        self.assertEqual(follow.target, self.band)
