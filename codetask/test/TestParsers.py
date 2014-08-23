# -*- coding: utf-8 -*-
from django.test import TestCase

from codetask.parsers import (get_parser_for_filename, BaseParser,
                              PythonParser, RubyParser)


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

    ('[](joey)', {'text': '', 'closed': False, 'username': 'joey'}),
    ('[](joey@no)', {'text': '', 'closed': False, 'username': 'joey@no'}),
    ('[](dee dee):', {'text': '', 'closed': False, 'username': 'dee dee'}),
    ('[x](mark)', {'text': '', 'closed': True, 'username': 'mark'}),
    ('[x](C. J.)', {'text': '', 'closed': True, 'username': 'C. J.'}),
)


COLON_TEXTS = (
    ('todo:', {'text': '', 'username': '', 'label': 'todo'}),
    ('TODO:', {'text': '', 'username': '', 'label': 'todo'}),
    ('   tOdO:', {'text': '', 'username': '', 'label': 'todo'}),

    ('todo:some task', {'text': 'some task', 'username': '', 'label': 'todo'}),
    ('tod: some task', {'text': 'some task', 'username': '', 'label': 'tod'}),

    ('todo(joey):', {'text': '', 'username': 'joey', 'label': 'todo'}),
    ('todo (joey):', {'text': '', 'username': 'joey', 'label': 'todo'}),
    ('todo(joey ):', {'text': '', 'username': 'joey', 'label': 'todo'}),
    ('todo (joey ):', {'text': '', 'username': 'joey', 'label': 'todo'}),
    ('todo(joey): some task', {'text': 'some task', 'username': 'joey',
                               'label': 'todo'}),
)


class TestParsers(TestCase):

    def test_get_parser_for_filename(self):
        Parser = get_parser_for_filename('file.py')
        self.assertEqual(Parser, PythonParser)

    def test_parse_username(self):
        parser = BaseParser('')
        texts = (
            ('andre', 'andre'),
            ('andre farzat', 'andre farzat'),
            ('(andré farzat)', 'andré farzat'),
            ('(andre )', 'andre'),
        )

        for text, expected in texts:
            self.assertEqual(parser.parse_username(text), expected)


class TestParsers_parse_text(TestCase):

    def test_squared_cases(self):
        for text, expected in SQUARED_TEXTS:
            parser = BaseParser(text)
            self.assertEqual(parser.text, expected['text'])
            self.assertEqual(parser.closed, expected['closed'])
            self.assertEqual(parser.username, expected['username'])

    def test_colon_cases(self):
        for text, expected in COLON_TEXTS:
            parser = BaseParser(text)
            self.assertEqual(parser.text, expected['text'])
            self.assertEqual(parser.label, expected['label'])
            self.assertEqual(parser.username, expected['username'])


class TestPythonParser(TestCase):

    def test_remove_markers(self):
        parser = PythonParser('#oi')
        self.assertEqual(parser._text, 'oi')

        parser = PythonParser('""" oi """')
        self.assertEqual(parser._text, 'oi')


class TestRubyParser(TestCase):

    def test_remove_markers(self):
        parser = RubyParser('#oi')
        self.assertEqual(parser._text, 'oi')
