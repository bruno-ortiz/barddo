from django.core.urlresolvers import reverse
from django.test import TestCase


class TestCoreViews(TestCase):
    def test_render_index_when_user_is_logged(self):
        logged = self.client.login(username='test', password='test')
        self.assertTrue(logged, 'User should be logged')
        response = self.client.get(reverse('core.views.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_render_index_when_user_is_not_logged(self):
        response = self.client.get(reverse('core.views.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_render_collection_create(self):
        logged = self.client.login(username='test', password='test')
        self.assertTrue(logged, 'User should be logged')
        response = self.client.get(reverse('core.views.create_collection'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'artist_dashboard.html')

    def test_redirect_collection_create_when_user_not_logged(self):
        response = self.client.get(reverse('core.views.create_collection'))
        self.assertRedirects(response, reverse('core.views.index') + '?next=/collections/create')