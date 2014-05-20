# coding=utf-8
import json
from urllib2 import urlopen, HTTPError, Request
import datetime

from PIL import Image
from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from facepy.graph_api import GraphAPI
from social.backends import google
from social.backends.facebook import FacebookOAuth2
from django.conf import settings

from signals import account_created
from accounts.models import BarddoUserProfile


GOOGLE_PLUS_BASE_URL = 'https://www.googleapis.com/plus/v1/people/{}'


def post_user_creation(backend, user, response, is_new=False, **kwargs):
    if is_new:
        account_created.send(user, user=user)
        # TODO: send a welcome message


def get_avatar(backend, user, response, is_new=False, **kwargs):
    """
    User authentication pipeline step to get user picture from social network, only on first login
    """
    if is_new:
        url = None
        if backend.__class__ is FacebookOAuth2:
            url = "http://graph.facebook.com/{0}/picture?type=large".format(response["id"])
        elif backend.__class__ is google.GooglePlusAuth and "picture" in response:
            url = response["picture"]

        if url:
            try:
                avatar = urlopen(url).read()
            except HTTPError:
                avatar = Image.open(settings.STATIC_URL + 'avatars/unknown_avatar.png')
            profile = BarddoUserProfile(user=user)
            profile.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar))
            profile.save()


def get_birth_date(backend, user, response, is_new=False, **kwargs):
    """
    User authentication pipeline step to get user birthday from social network, only on first login
    """
    # TODO: better handling date masks
    if is_new:
        birth_date = None
        if backend.__class__ is FacebookOAuth2:
            birth_date = datetime.datetime.strptime(response['birthday'], '%m/%d/%Y').date()
        elif backend.__class__ is google.GooglePlusAuth:
            user_id = response['id']
            data = __get_google_plus_data(GOOGLE_PLUS_BASE_URL.format(user_id), response['access_token'])
            birth_date = datetime.datetime.strptime(data.get('birthday', '2014-01-17'), '%Y-%m-%d').date()
        if birth_date:
            profile = user.profile
            profile.birth_date = birth_date
            profile.save()


def get_gender(backend, user, response, is_new=False, **kwargs):
    """
    User authentication pipeline step to get user gender from social network, only on first login
    """
    if is_new:
        gender = None
        if backend.__class__ is FacebookOAuth2:
            gender = response['gender'][:1]
        elif backend.__class__ is google.GooglePlusAuth:
            gender = response['gender'][:1]
        if gender:
            profile = user.profile
            profile.gender = gender.upper()
            profile.save()


def get_country(backend, user, response, is_new=False, **kwargs):
    """
    User authentication pipeline step to get user country from social network, only on first login
    """
    if is_new:
        country = None
        if backend.__class__ is FacebookOAuth2:
            graph = GraphAPI(oauth_token=response['access_token'])
            country_query = graph.fql(r'SELECT current_location FROM user WHERE uid=me()')
            country = country_query['data'][0]['current_location']['country']
        elif backend.__class__ is google.GooglePlusAuth:
            country = 'Brazil'  # TODO: google plus doesn't provide user country?

        if country:
            profile = user.profile
            profile.country = country
            profile.save()


def __get_google_plus_data(url, access_token):
    """
    Request custom g+ information
    """
    request = Request(url, headers={"Authorization": "Bearer {}".format(access_token)})
    return json.loads(urlopen(request).read())