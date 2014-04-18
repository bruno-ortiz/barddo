# coding=utf-8
from PIL import Image
from urllib2 import urlopen, HTTPError
import datetime

from django.core.files.base import ContentFile
from django.template.defaultfilters import slugify
from facepy.graph_api import GraphAPI
from social.backends import google
from social.backends.facebook import FacebookOAuth2

from accounts.models import BarddoUserProfile


__author__ = 'bruno'


def get_avatar(backend, user, response, is_new=False, **kwargs):
    if is_new:
        url = None
        if backend.__class__ is FacebookOAuth2:
            url = "http://graph.facebook.com/{0}/picture?type=large".format(response["id"])
        elif backend.__class__ is google.GoogleOAuth2 and "picture" in response:
            url = response["picture"]
        if url:
            try:
                avatar = urlopen(url).read()
            except HTTPError:
                avatar = Image.open('/assets/avatars/avatar2.png')
            profile = BarddoUserProfile(user=user)
            profile.avatar.save(slugify(user.username + " social") + '.jpg', ContentFile(avatar))
            profile.save()


def get_birth_date(backend, user, response, is_new=False, **kwargs):
    if is_new:
        birth_date = None
        if backend.__class__ is FacebookOAuth2:
            birth_date = response['birthday']
        elif backend.__class__ is google.GoogleOAuth2:
            # TODO: birthday está disponivel apenas no google-plus, porem o django-social-auth busca apenas informações do google
            birth_date = '02/15/1990'  # default date
        if birth_date:
            profile = user.user_profile
            profile.birth_date = datetime.datetime.strptime(birth_date, '%m/%d/%Y').date()
            profile.save()


def get_gender(backend, user, response, is_new=False, **kwargs):
    if is_new:
        gender = None
        if backend.__class__ is FacebookOAuth2:
            gender = response['gender'][:1]
        elif backend.__class__ is google.GoogleOAuth2:
            gender = response['gender'][:1]
        if gender:
            profile = user.user_profile
            profile.gender = gender.upper()
            profile.save()


def get_country(backend, user, response, is_new=False, **kwargs):
    if is_new:
        country = None
        if backend.__class__ is FacebookOAuth2:
            graph = GraphAPI(oauth_token=response['access_token'])
            country_query = graph.fql(r'SELECT current_location FROM user WHERE uid=me()')
            country = country_query['data'][0]['current_location']['country']
        elif backend.__class__ is google.GoogleOAuth2:
            country = 'Brazil'
        if country:
            profile = user.user_profile
            profile.country = country
            profile.save()