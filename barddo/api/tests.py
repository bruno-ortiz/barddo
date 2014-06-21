# coding=utf-8

from rest_framework.test import APITestCase

from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from feed.models import JoinAction, UserFeed

from api.serializers import UserFriendsSerializer, UserFeedSerializer

from accounts.models import BarddoUser
from follow.models import Follow


class RestAPITest(APITestCase):
    fixtures = ['sample_user_and_profile.json']

    def setUp(self):
        super(RestAPITest, self).setUp()
        self.beavis = BarddoUser.objects.get(pk=1)
        self.beavis_token = Token.objects.create(user=self.beavis)
        beavis_action = JoinAction.objects.create()
        self.beavis_feed = UserFeed.objects.create(user=self.beavis, action=beavis_action)

        self.butthead = BarddoUser.objects.get(pk=2)
        butthead_action = JoinAction.objects.create()
        self.bbutthead_feed = UserFeed.objects.create(user=self.butthead, action=butthead_action)

        self.wolverine = BarddoUser.objects.get(pk=3)

        self.client.logout()

    def test_list_user_friends(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.beavis_token.key)
        Follow.objects.add_follower(follower=self.beavis, followee=self.butthead)

        url = reverse('user-friends-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, "Só deveria ter retornado um usuário")
        self.assertEqual(response.data[0].keys(), ['id', 'name', 'picture'])
        self.assertEqual(response.data[0], UserFriendsSerializer(self.butthead).data)

    def test_list_user_friends_access(self):
        url = reverse('user-friends-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_user_feed(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.beavis_token.key)

        url = reverse('user-feed-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1, "Só deveria ter retornado um feed")
        self.assertEqual(response.data[0].keys(), ['id', 'created', 'picture', 'message'])
        self.assertEqual(response.data[0], UserFeedSerializer(self.beavis_feed).data)

    def test_list_user_feed_access(self):
        url = reverse('user-feed-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # TODO: test work access

    def test_list_user_favorites_access(self):
        url = reverse('user-favorites-list')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)