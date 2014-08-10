# coding=utf-8
from django.core.files.images import ImageFile

from django.test import TestCase
from mock import Mock
from model_mommy import mommy

from core.models import Work, WorkPage


class WorkTest(TestCase):
    def setUp(self):
        self.work = mommy.make(Work)
        mock_image = Mock(spec=ImageFile)
        mock_image.name = "batatinha.png"
        mock_image.read.return_value = ""
        for i in xrange(0, 5):
            self.work.add_page(mock_image)

    def test_pages_added(self):
        self.assertEqual(len(self.work.pages), WorkPage.objects.all().count())

    def test_can_move_pages(self):
        page_1 = WorkPage.objects.get(id=1)
        page_2 = WorkPage.objects.get(id=2)
        self.assertEqual(page_1.sequence, 0)
        self.assertEqual(page_2.sequence, 1)

        self.work.move_page(0, 2)

        # Aqui a página com id 1 foi movida para a posição 2 enquanto a página com id 2 foi desceu uma posição e está na posição 0
        page_1 = WorkPage.objects.get(id=1)
        page_2 = WorkPage.objects.get(id=2)
        self.assertEqual(page_1.sequence, 2)
        self.assertEqual(page_2.sequence, 0)

        page_5 = WorkPage.objects.get(id=5)
        self.assertEqual(page_5.sequence, 4)

        self.work.move_page(4, 2)

        # Aqui a página com id 5 foi movida para a posição 2 enquanto a página com id 1 foi subiu uma posição e está na posição 3
        page_1 = WorkPage.objects.get(id=1)
        page_5 = WorkPage.objects.get(id=5)
        self.assertEqual(page_5.sequence, 2)
        self.assertEqual(page_1.sequence, 3)

    def test_can_remove_page(self):
        self.assertEqual(5, len(self.work.pages))
        page_2 = WorkPage.objects.get(id=2)
        self.assertEqual(page_2.sequence, 1)

        # remove a página na posição 0
        self.work.remove_page(0)

        # verifica que a página de id 2 anteriormente na posição 1 agora se encontra na posição 0
        self.assertEqual(4, len(self.work.pages))
        page_2 = WorkPage.objects.get(id=2)
        self.assertEqual(page_2.sequence, 0)
