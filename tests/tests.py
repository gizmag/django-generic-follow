from django.test import TestCase
from django.contrib.auth.models import User
from generic_follow.models import Follow
from .models import Band


class GenericFollowUserMixinTests(TestCase):
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

    def test_calling_follow_multiple_times_doesnt_create_multiple_follows(self):
        self.user.follow(self.band)
        self.assertEqual(1, Follow.objects.count())

        self.user.follow(self.band)
        self.assertEqual(1, Follow.objects.count())

    def test_user_can_unfollow_successfully(self):
        self.user.follow(self.band)
        self.assertEqual(1, Follow.objects.count())

        self.user.unfollow(self.band)
        self.assertEqual(0, Follow.objects.count())

    def test_calling_unfollow_multiple_times_doesnt_cause_errors(self):
        self.user.follow(self.band)
        self.assertEqual(1, Follow.objects.count())

        self.user.unfollow(self.band)
        self.assertEqual(0, Follow.objects.count())

        self.user.unfollow(self.band)
        self.user.unfollow(self.band)
        self.user.unfollow(self.band)
        self.user.unfollow(self.band)
        self.assertEqual(0, Follow.objects.count())

    def test_is_following_returns_correct_result(self):
        self.assertFalse(self.user.is_following(self.band))

        self.user.follow(self.band)
        self.assertTrue(self.user.is_following(self.band))

        self.user.unfollow(self.band)
        self.assertFalse(self.user.is_following(self.band))
