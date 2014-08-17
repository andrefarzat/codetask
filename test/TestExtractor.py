import os
from unittest import TestCase
from pygments.token import Token

from codetask.extractor import Extractor


BASE_DIR = os.path.join(os.path.dirname(__file__), 'mockproj')


class TestExtractor(TestCase):
    python_file = os.path.join(BASE_DIR, 'python.py')

    def test_file_content_property(self):
        with open(self.python_file) as f:
            file_content = f.read()

        extractor = Extractor(self.python_file)
        self.assertEqual(file_content, extractor.file_content)

    def test_get_valid_tokens(self):
        """Should return only comments tokens"""
        extractor = Extractor(self.python_file)

        tokens = extractor.get_valid_tokens()

        first_token = tokens.next()
        self.assertEqual(first_token['token'], Token.Comment)
        self.assertEqual(first_token['text'], '# todo: nothing')
        self.assertEqual(first_token['line_number'], 6)

        second_token = tokens.next()
        self.assertEqual(second_token['token'], Token.Comment)
        self.assertEqual(second_token['text'], '# fixme: opa')
        self.assertEqual(second_token['line_number'], 9)

    def test__get_initial_line_number(self):
        extractor = Extractor(self.python_file)

        self.assertEqual(3, extractor._get_initial_line_number())