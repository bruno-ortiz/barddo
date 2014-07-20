# coding=utf-8
from django.test import TestCase

from accounts.models import BarddoUser
from follow.models import Follow
from publishing.models import PublishingHouse


class FollowingManagerTest(TestCase):
    fixtures = ['load_test_publishers.json', 'sample_user_and_profile.json']

    def setUp(self):
        super(FollowingManagerTest, self).setUp()
        self.beavis = BarddoUser.objects.get(pk=1)
        self.butthead = BarddoUser.objects.get(pk=2)
        self.shounen_jump = PublishingHouse.objects.get(pk=1)
        self.hakusensha = PublishingHouse.objects.get(pk=2)

    def test_user_can_follow_publisher(self):
        Follow.objects.add_follower(follower=self.beavis, followee=self.shounen_jump)
        Follow.objects.add_follower(follower=self.beavis, followee=self.hakusensha)
        Follow.objects.add_follower(follower=self.butthead, followee=self.hakusensha)

        self.assertTrue(Follow.objects.follows(self.beavis, self.hakusensha))

        following_publishers = Follow.objects.following(self.beavis, PublishingHouse)
        self.assertIs(len(following_publishers), 2, 'Beavis deveria seguir apenas 2 editoras')
        self.assertIn(self.shounen_jump, following_publishers)
        self.assertIn(self.hakusensha, following_publishers)

        following_publishers = Follow.objects.following(self.butthead, PublishingHouse)
        self.assertIs(len(following_publishers), 1, 'Butthead deveria seguir apenas 1 editora')
        self.assertIn(self.hakusensha, following_publishers)

        self.assertTrue(Follow.objects.follows(self.beavis, self.hakusensha))

    def test_user_can_follow_user(self):
        Follow.objects.add_follower(follower=self.beavis, followee=self.butthead)
        Follow.objects.add_follower(follower=self.butthead, followee=self.beavis)

        following_users = Follow.objects.following(self.beavis, BarddoUser)
        self.assertIs(len(following_users), 1, 'Beavis deveria seguir Butthead')
        self.assertEqual(following_users[0], self.butthead, 'Beavis deveria seguir Butthead')

        following_users = Follow.objects.following(self.butthead, BarddoUser)
        self.assertIs(len(following_users), 1, 'Butthead deveria seguir Beavis')
        self.assertEqual(following_users[0], self.beavis, 'Beavis deveria seguir Butthead')

        self.assertTrue(Follow.objects.follows(self.beavis, self.butthead))

    def test_user_can_follow_multiple_types(self):
        Follow.objects.add_follower(follower=self.beavis, followee=self.butthead)
        Follow.objects.add_follower(follower=self.butthead, followee=self.beavis)
        Follow.objects.add_follower(follower=self.beavis, followee=self.shounen_jump)
        Follow.objects.add_follower(follower=self.beavis, followee=self.hakusensha)
        Follow.objects.add_follower(follower=self.butthead, followee=self.hakusensha)

        following_publishers = Follow.objects.following(self.beavis, PublishingHouse)
        self.assertIs(len(following_publishers), 2, 'Beavis deveria seguir apenas 2 editoras')
        self.assertIn(self.shounen_jump, following_publishers)
        self.assertIn(self.hakusensha, following_publishers)

        following_publishers = Follow.objects.following(self.butthead, PublishingHouse)
        self.assertIs(len(following_publishers), 1, 'Butthead deveria seguir apenas 1 editora')
        self.assertIn(self.hakusensha, following_publishers)

        following_users = Follow.objects.following(self.beavis, BarddoUser)
        self.assertIs(len(following_users), 1, 'Beavis deveria seguir Butthead')
        self.assertEqual(following_users[0], self.butthead, 'Beavis deveria seguir Butthead')

        following_users = Follow.objects.following(self.butthead, BarddoUser)
        self.assertIs(len(following_users), 1, 'Butthead deveria seguir Beavis')
        self.assertEqual(following_users[0], self.beavis, 'Beavis deveria seguir Butthead')

    def test_cache_is_being_correctly_used(self):
        Follow.objects.add_follower(follower=self.beavis, followee=self.hakusensha)
        with self.assertNumQueries(2):
            Follow.objects.following(self.beavis, PublishingHouse)
            Follow.objects.following(self.beavis, PublishingHouse)

        #Adding a follower of the same type busts the cache and the query must be done again
        Follow.objects.add_follower(follower=self.beavis, followee=self.shounen_jump)
        with self.assertNumQueries(2):
            Follow.objects.following(self.beavis, PublishingHouse)
            Follow.objects.following(self.beavis, PublishingHouse)

        #Adding a follower from a different type doesn't busts the cache
        Follow.objects.add_follower(follower=self.beavis, followee=self.butthead)
        with self.assertNumQueries(0):
            Follow.objects.following(self.beavis, PublishingHouse)

    def test_can_unfollow(self):
        """
        Neste teste Butthead compartilham o mesmo id no banco de dados, porém são de tipos diferentes,
        assim eu testo que o método de unfollow leva em consideração o tipo também.
        """
        Follow.objects.add_follower(follower=self.beavis, followee=self.butthead)
        Follow.objects.add_follower(follower=self.beavis, followee=self.hakusensha)

        Follow.objects.remove_follower(self.beavis, self.butthead)

        follows_butthead = Follow.objects.follows(self.beavis, self.butthead)
        self.assertFalse(follows_butthead, msg='Beavis não deveria seguir butthead')

        follows_hakusensha = Follow.objects.follows(self.beavis, self.hakusensha)
        self.assertTrue(follows_hakusensha, msg='Beavis deveria seguir hakusenha')