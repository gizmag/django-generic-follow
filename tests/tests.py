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
        self.photog = Photographer.objects.create(name='Henri Cartier-Bresson')

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
        self.user.follow(self.band)
        self.user.follow(self.photog)

        result = self.user.get_follow_set()
        self.assertEqual(result, [self.band, self.photog])

    def test_get_follow_set_filters_by_model_type_if_provided(self):
        self.user.follow(self.band)
        self.user.follow(self.photog)

        self.assertEqual(self.user.get_follow_set(Photographer), [self.photog])

    def test_user_cant_follow_same_object_twice(self):
        self.user.follow(self.band)
        Follow.objects.update_batch(target=self.band,
                                    users_follow=[(self.user, True)])
        self.assertEqual(1, len(self.band.get_follower_set()))


class GenericFollowTargetMixin(TestCase):
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

    def test_get_follower_set_returns_followers(self):
        self.user.follow(self.band)
        self.assertEqual(1, len(self.band.get_follower_set()))

        self.user2.follow(self.band)
        self.assertEqual(2, len(self.band.get_follower_set()))


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

    def test_update_batch_with_user_not_currently_following_and_set_to_true_creates_follow(self):
        Follow.objects.update_batch(
            users_follow=[(self.user, True)],
            target=self.band
        )
        self.assertEqual(1, Follow.objects.count())

    def test_update_batch_with_user_not_currently_following_and_set_to_false_does_nothing(self):
        Follow.objects.update_batch(
            users_follow=[(self.user, False)],
            target=self.band
        )
        self.assertEqual(0, Follow.objects.count())

    def test_update_batch_with_user_currently_following_and_set_to_false_deletes_follow(self):
        self.user.follow(self.band)
        Follow.objects.update_batch(
            users_follow=[(self.user, False)],
            target=self.band
        )
        self.assertEqual(0, Follow.objects.count())

    def test_update_batch_with_user_currently_following_and_set_to_true_does_nothing(self):
        self.user.follow(self.band)
        Follow.objects.update_batch(
            users_follow=[(self.user, True)],
            target=self.band
        )
        self.assertEqual(1, Follow.objects.count())
