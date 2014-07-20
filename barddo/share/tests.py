from django.test import TestCase

from django.test.client import RequestFactory
from django.db import models

import templatetags.social_share

from templatetags.social_share import _build_url, post_to_twitter, post_to_facebook, post_to_gplus


class SampleModel(models.Model):
    image = models.ImageField(upload_to='images')

    def get_absolute_url(self):
        return "/some/mock/test/url"

    class Meta:
        app_label = 'test'


class TestShareViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_can_render_absolute_raw_url(self):
        request = self.factory.get('/test')
        result = _build_url(request, "/some_url")
        self.assertEqual(result, "http://testserver/some_url")

    def test_can_render_absolute_image_url(self):
        request = self.factory.get('/test')

        sample = SampleModel()
        sample.image = "tmp/test1.jpg"

        result = _build_url(request, sample.image)
        self.assertEqual(result, "http://testserver/media/tmp/test1.jpg")

    def test_can_render_absolute_model_url_without_bitly(self):
        request = self.factory.get('/test')

        old_value = templatetags.social_share.DJANGO_BITLY
        try:
            sample = SampleModel()
            templatetags.social_share.DJANGO_BITLY = False
            result = _build_url(request, sample)
        finally:
            templatetags.social_share.DJANGO_BITLY = old_value

        self.assertEqual(result, "http://testserver" + sample.get_absolute_url())

    def test_can_render_absolute_model_url_with_bitly(self):
        request = self.factory.get('/test')

        old_value = templatetags.social_share.DJANGO_BITLY
        try:
            sample = SampleModel()
            sample.id = 1
            templatetags.social_share.DJANGO_BITLY = True
            result = _build_url(request, sample)
        finally:
            templatetags.social_share.DJANGO_BITLY = old_value

        self.assertTrue(result.startswith('http://bit.ly/'))

    def test_can_render_twitter_url(self):
        sample = SampleModel()
        sample.id = 1

        old_value = templatetags.social_share.DJANGO_BITLY
        try:
            templatetags.social_share.DJANGO_BITLY = True
            context = post_to_twitter({}, "twitt", sample, "test twitter")
        finally:
            templatetags.social_share.DJANGO_BITLY = old_value

        self.assertEqual(context['link_text'], "test twitter")

        self.assertTrue(context['full_text'].startswith('twitt'))
        self.assertTrue(context['tweet_url'].startswith('http://twitter.com/intent/tweet'))

    def test_can_render_facebook_url(self):
        sample = SampleModel()
        sample.id = 1
        context = post_to_facebook({}, sample, "test facebook")

        self.assertEqual(context['link_text'], "test facebook")
        self.assertTrue(context['facebook_url'].startswith('http://www.facebook.com/sharer/sharer.php'))

    def test_can_render_gplus_url(self):
        sample = SampleModel()
        sample.id = 1
        context = post_to_gplus({}, sample, "test google")

        self.assertEqual(context['link_text'], "test google")
        self.assertTrue(context['gplus_url'].startswith('https://plus.google.com/share'))

