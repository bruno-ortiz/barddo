from django.test import TestCase

__author__ = 'bruno'


class FollowingManagerTest(TestCase):
    fixtures = ['load_test_publishers.json', 'sample_user_and_profile.json']

    def setUp(self):
        super(FollowingManagerTest, self).setUp()

    def test_follow(self):
        pass