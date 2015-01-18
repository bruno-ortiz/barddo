# coding=utf-8
import unittest
from mangashost.manga_parser import MangaParser


class MangaParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = MangaParser()

    def test_can_fetch_manga_detail(self):
        name, data = self.parser.extract_manga_data(u"http://br.mangahost.com/manga/rain")
        self.assertEqual(name, u"-rain-")
        self.assertEqual(data['cover'], u"http://img.mangahost.com/br/mangas_files/rain/image_rain_large.jpg")
        self.assertEqual(data['author'], u'Hashiba Hayase')
        self.assertEqual(data['tags'], [u"escolar", u"shoujo ai", u"sobrenatural"])
        self.assertEqual(data['status'], u"Completo")
        self.assertIn(u'Em um dia chuvoso, ', data['sinopse'])
        self.assertTrue(len(data['chapters']) == 1)

    def test_can_fetch_one_piece_detail(self):
        name, data = self.parser.extract_manga_data(u"http://br.mangahost.com/manga/one-piece-pt-br")
        self.assertEqual(name, u"One Piece (PT-BR)")
        self.assertEqual(data['cover'], u"http://img.mangahost.com/br/mangas_files/one-piece-pt-br/image_one-piece-pt-br_large.jpg")
        self.assertEqual(data['author'], u'Oda Eiichiro')
        self.assertEqual(data['tags'], [u"acao", u"aventura", u"comedia", u"fantasia", u"shounen", u"super poderes"])
        self.assertEqual(data['status'], u"Ativo")
        self.assertIn(u'One Piece começa quando Gol D. Roger, o Rei Dos Piratas', data['sinopse'])
        self.assertTrue(len(data['chapters']) >= 773)

    def test_can_fetch_custom_detail(self):
        name, data = self.parser.extract_manga_data(u"http://br.mangahost.com/manga/bleach-pt-br")
        self.assertEqual(name, u"Bleach (PT-BR)")
        self.assertEqual(data['cover'], u"http://img.mangahost.com/br/mangas_files/bleach-pt-br/image_bleach-pt-br_large.jpg")
        self.assertEqual(data['author'], u'Tite Kubo')
        self.assertEqual(data['tags'], [u"acao", u"comedia", u"shounen", u"sobrenatural", u"super poderes"])
        self.assertEqual(data['status'], u"Ativo")
        self.assertIn(u'Kurosaki Ichigo é um estudante de 15 anos que tem uma estranha capacidade de ver', data['sinopse'])
        self.assertTrue(len(data['chapters']) >= 611)