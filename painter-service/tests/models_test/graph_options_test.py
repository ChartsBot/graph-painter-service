import unittest
from pprint import pprint

from models.graph_options import GraphOption
from models.themes import DarkTheme


class TestGraphOptions(unittest.TestCase):

    def test_serializing(self):
        theme = {'theme_name': 'dark'}
        g = GraphOption(**theme)
        self.assertEqual(g.theme.__class__, DarkTheme.__class__)
        self.assertEqual('dark', g.theme_name)
        g = GraphOption(theme_name='dark')
        pprint(g)
        pprint(g.dict())

