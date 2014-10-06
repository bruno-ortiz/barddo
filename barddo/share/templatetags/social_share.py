# -*- coding: utf-8 -*-
from django import template
from django.contrib.sites.models import Site
from django.db.models import Model
from django.db.models.fields.files import ImageFieldFile
from django.template.defaultfilters import urlencode
from django.conf import settings
from django.utils.translation import ugettext as _

from core.models import Collection

register = template.Library()

TWITTER_ENDPOINT = 'http://twitter.com/intent/tweet?text=%s'
FACEBOOK_ENDPOINT = 'http://www.facebook.com/sharer/sharer.php?u=%s'
GOOGLEPLUS_ENDPOINT = 'https://plus.google.com/share?url=%s'


@register.inclusion_tag('social_imports.html')
def social_imports():
    return {"facebook_id": settings.SOCIAL_AUTH_FACEBOOK_KEY}


def compile_text(context, text):
    ctx = template.context.Context(context)
    return template.Template(text).render(ctx)


class MockRequest(object):
    def build_absolute_uri(self, relative_url):
        if relative_url.startswith('http'):
            return relative_url
        current_site = Site.objects.get_current()
        return '%s%s' % (current_site.domain, relative_url)


def _build_url(request, obj_or_url, force_raw=False):
    if obj_or_url is not None:
        if isinstance(obj_or_url, ImageFieldFile):
            return request.build_absolute_uri(obj_or_url.url)
        elif isinstance(obj_or_url, Model):
            return request.build_absolute_uri(obj_or_url.get_absolute_url())
        else:
            return request.build_absolute_uri(obj_or_url)
    return ''


def _compose_tweet(text, url=None):
    if url is None:
        url = ''

    text = _("Wow, nice! See this work on Barddo!\n") + text + "\n"

    total_length = len(text) + len(' ') + len(url)

    if total_length > 140:
        truncated_text = text[:(140 - len(url))] + u"…"
    else:
        truncated_text = text
    return truncated_text


@register.simple_tag(takes_context=True)
def post_to_twitter_url(context, text, obj_or_url=None):
    text = compile_text(context, text)
    request = context.get('request', MockRequest())

    url = _build_url(request, obj_or_url)

    tweet = _compose_tweet(text, url)
    custom_parameters = "&hashtags=barddo"
    context['tweet_url'] = TWITTER_ENDPOINT % urlencode(tweet) + custom_parameters
    return context


@register.inclusion_tag('share/post_to_twitter.html', takes_context=True)
def post_to_twitter(context, obj=None, link_text='Post to Twitter'):
    if isinstance(obj, Collection):
        text = obj.name
    else:
        text = obj.collection.name + " - " + obj.title
    context = post_to_twitter_url(context, text, obj)
    request = context.get('request', MockRequest())
    url = _build_url(request, obj, True)
    tweet = _compose_tweet(text, url)  # TODO: Melhorar compose tweet

    context['link_text'] = link_text
    context['full_text'] = tweet
    return context


@register.inclusion_tag('share/post_local_twitter.html', takes_context=True)
def post_to_twitter_fake(context, work=None, link_text='Post to Twitter'):
    return post_to_twitter(context, work, link_text)


@register.simple_tag(takes_context=True)
def post_to_facebook_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['facebook_url'] = FACEBOOK_ENDPOINT % urlencode(url)
    context['url'] = _build_url(request, obj_or_url, True)
    return context


@register.inclusion_tag('share/post_to_facebook.html', takes_context=True)
def post_to_facebook(context, obj_or_url=None, link_text='Post to Facebook'):
    context = post_to_facebook_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.inclusion_tag('share/post_local_facebook.html', takes_context=True)
def post_to_facebook_fake(context, obj_or_url=None, link_text='Post to Facebook'):
    return post_to_facebook(context, obj_or_url, link_text)


@register.simple_tag(takes_context=True)
def post_to_gplus_url(context, obj_or_url=None):
    request = context.get('request', MockRequest())
    url = _build_url(request, obj_or_url)
    context['gplus_url'] = GOOGLEPLUS_ENDPOINT % urlencode(url)
    context['url'] = _build_url(request, obj_or_url, True)
    return context


@register.inclusion_tag('share/post_to_google_plus.html', takes_context=True)
def post_to_gplus(context, obj_or_url=None, link_text='Post to GooglePlus'):
    context = post_to_gplus_url(context, obj_or_url)
    context['link_text'] = link_text
    return context


@register.inclusion_tag('work-open-graph.html', takes_context=True)
def render_work_opengraph_header(context, work):
    request = context.get('request', MockRequest())

    context['facebook_api_key'] = settings.SOCIAL_AUTH_FACEBOOK_KEY
    context['facebook_app_name'] = settings.FACEBOOK_APP_NAME
    context['work_url'] = _build_url(request, work, True)
    context['work_title'] = work.title

    if work.cover_url:
        context['work_image'] = work.cover_url
    else:
        context['work_image'] = _build_url(request, work.cover)

    context['work_description'] = work.summary
    context['collection_name'] = work.collection.name
    context['artist_name'] = work.author.get_full_name()

    return context


@register.inclusion_tag('collection-open-graph.html', takes_context=True)
def render_collection_opengraph_header(context, collection):
    request = context.get('request', MockRequest())

    context['facebook_api_key'] = settings.SOCIAL_AUTH_FACEBOOK_KEY
    context['facebook_app_name'] = settings.FACEBOOK_APP_NAME
    context['collection_url'] = _build_url(request, collection, True)
    context['collection_name'] = collection.name

    if collection.cover_url:
        context['collection_cover'] = collection.cover_url
    else:
        context['collection_cover'] = _build_url(request, collection.cover)
    context['collection_description'] = collection.summary
    context['artist_name'] = collection.author.get_full_name()

    return context


class UnsupportedTwitterModel(Exception):
    pass