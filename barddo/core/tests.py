from django.test import TestCase


class TestCoreViews(TestCase):
    fixtures = ["sample_user_and_profile.json"]

    # TODO: create a new set of relevant tests
    def test_mock(self):
        self.assertTrue(1 + 1, 2)
