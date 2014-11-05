# coding=utf-8
import unittest

from crawler.centraldemangas.manga_parser import MangaParser


class MangaParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = MangaParser()

    def test_can_fetch_manga_detail(self):
        name, data = self.parser.extract_manga_data(u"http://centraldemangas.net/mangas/info/6-no-trigger")
        self.assertEqual(name, u"6 no Trigger")
        self.assertEqual(data['cover'], u"http://capas.centraldemangas.com.br/150x200/6-no-trigger.jpg")
        self.assertEqual(data['author'], u'Tali')
        self.assertEqual(data['tags'], [u"Ação", u"Shounen"])
        self.assertEqual(data['status'], u"Em publicação")
        self.assertIn(u'Uma única história sobre o "assassino de aluguel"', data['sinopse'])
        self.assertTrue(len(data['chapters']) >= 5)

    def test_can_fetch_one_piece_detail(self):
        name, data = self.parser.extract_manga_data(u"http://centraldemangas.net/mangas/info/one-piece")
        self.assertEqual(name, u"One Piece")
        self.assertEqual(data['cover'], u"http://capas.centraldemangas.com.br/150x200/one-piece.jpg")
        self.assertEqual(data['author'], u'Eiichiro Oda')
        self.assertEqual(data['tags'], [u"Ação", u"Aventura", u"Comédia", u"Fantasia", u"Shounen"])
        self.assertEqual(data['status'], u"Em publicação")
        self.assertIn(u'One Piece começa quando Gol D. Roger, o Rei Dos Piratas', data['sinopse'])
        self.assertTrue(len(data['chapters']) >= 700)

    def test_can_fetch_custom_detail(self):
        name, data = self.parser.extract_manga_data(u"http://centraldemangas.net/mangas/info/bleach")
        self.assertEqual(name, u"Bleach")
        self.assertEqual(data['cover'], u"http://capas.centraldemangas.com.br/150x200/bleach.jpg")
        self.assertEqual(data['author'], u'Tite Kubo')
        self.assertEqual(data['tags'], [u"Ação", u"Comédia", u"Fantasia", u"Shounen", u"Sobrenatural"])
        self.assertEqual(data['status'], u"Em publicação")
        self.assertIn(u'Ichigo Kurosaki um garoto de 15 anos que tem uma estranha', data['sinopse'])
        self.assertTrue(len(data['chapters']) >= 600)