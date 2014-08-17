from unittest import TestCase


class TestMatches(TestCase):
    """ Possible matches:
    [] text
    [] text
    [](username) text
    [](username): text
    [ ] text
    [ ](username): text """

    def test_nada(self):

        self.assertTrue(True)
