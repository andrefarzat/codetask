from django.test import TestCase

from codetask.parsers import get_parser_for_filename, BaseParser, PythonParser


SQUARED_TEXTS = (
    ('[]', {'text': '', 'closed': False, 'username': ''}),
    ('[]some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[]:some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[] some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[]: some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[ ]', {'text': '', 'closed': False, 'username': ''}),
    ('[ ]some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[ ]:some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[ ]: some task', {'text': 'some task', 'closed': False, 'username': ''}),
    ('[x]: some task', {'text': 'some task', 'closed': True, 'username': ''}),
)


class TestParsers(TestCase):

    def test_get_parser_for_filename(self):
        Parser = get_parser_for_filename('file.py')
        self.assertEqual(Parser, PythonParser)


class TestParsers_parse_text(TestCase):

    def test_squared_cases(self):
        for text, expected in SQUARED_TEXTS:
            parser = BaseParser(text)
            self.assertEqual(parser.text, expected['text'])
            self.assertEqual(parser.closed, expected['closed'])
