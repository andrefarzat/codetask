import os
from pygments.token import Token

from django.test import TestCase

from codetask.extractor import Extractor, ExtractedTask, DirExtractor


BASE_DIR = os.path.join(os.path.dirname(__file__), 'mockproj')


class TestDirExtractor(TestCase):

    def test___init__with_wrong_path(self):
        with self.assertRaises(ValueError):
            DirExtractor('')

    def test_get_extractors(self):
        dir_extractor = DirExtractor(BASE_DIR)
        for extractor in dir_extractor.get_extractors():
            self.assertEqual(extractor.__class__, Extractor)


class TestExtractor(TestCase):
    python_file = os.path.join(BASE_DIR, 'python.py')
    text_file = os.path.join(BASE_DIR, 'text.txt')

    def test___repr__(self):
        extractor = Extractor(self.python_file)

        self.assertEqual(extractor.__repr__(),
                         '<Extractor filepath=%s>' % self.python_file)

    def test_file_content_property(self):
        with open(self.python_file) as f:
            file_content = f.read()

        extractor = Extractor(self.python_file)
        self.assertEqual(file_content, extractor.file_content)

    def test___init___with_wrong_filepath(self):
        with self.assertRaises(ValueError):
            Extractor('')

    def test_get_valid_tokens(self):
        """Should return only comment tokens"""
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

        extractor = Extractor(self.text_file)
        self.assertEqual(1, extractor._get_initial_line_number())

    def test_get_tasks(self):
        extractor = Extractor(self.python_file)
        for task in extractor.get_tasks():
            self.assertEqual(task.__class__, ExtractedTask)


class TestExtractedTask(TestCase):

    def test_text(self):
        """given a whole line, it would return only the text of the task"""
        raw_text = '# todo: nothing'
        task = ExtractedTask(raw_text, 'python.py')

        self.assertEqual(task.raw_text, raw_text)
        self.assertEqual(task.text, 'nothing')
        self.assertEqual(task.label, 'todo')
        self.assertEqual(task.filepath, 'python.py')
