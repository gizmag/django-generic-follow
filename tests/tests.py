from django.test import TestCase
from django.contrib.auth.models import User
from generic_follow.models import Follow
from .models import Band, Photographer


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

    def test_get_follow_set_returns_all_obejcts_a_user_is_following(self):
        photog = Photographer.objects.create(name='Henri Cartier-Bresson')
        self.user.follow(self.band)
        self.user.follow(photog)

        result = self.user.get_follow_set()
        self.assertEqual(result, [self.band, photog])



class GenericFollowManagerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='john',
            password='password'
        )
        self.user2 = User.objects.create_user(
            username='jane',
            password='password'
        )
        self.band = Band.objects.create(name='Foals')

    def test_create_batch_creates_follows_for_all_users_passed_in(self):
        Follow.objects.create_batch(users=[self.user, self.user2], target=self.band)

        self.assertEqual(2, Follow.objects.count())

        self.assertTrue(Follow.objects.filter(user=self.user).exists())
        self.assertTrue(Follow.objects.filter(user=self.user2).exists())

    def test_delete_batch_deletes_follows_for_all_users_passed_in_related_to_target(self):
        band2 = Band.objects.create(name='Nirvana')

        Follow.objects.create_batch(users=[self.user, self.user2], target=self.band)
        self.user.follow(band2)

        self.assertEqual(3, Follow.objects.count())

        Follow.objects.delete_batch(users=[self.user, self.user2], target=self.band)

        self.assertEqual(1, Follow.objects.count())
