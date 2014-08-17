import os
import re
from pygments.lexers import get_lexer_for_filename
from pygments.token import Token


class Extractor:
    """Does the extration in one single file"""

    _initial_line_number_re = re.compile(r'^(\n+)')

    def __init__(self, filepath):
        if not os.path.isfile(filepath):
            raise ValueError("%s does not exist" % filepath)

        self.filepath = filepath
        self.lexer = get_lexer_for_filename(filepath)

    @property
    def file_content(self):
        if getattr(self, '_file_content', None) is None:
            with open(self.filepath) as f:
                self._file_content = f.read()
        return self._file_content

    def _get_initial_line_number(self):
        result = self._initial_line_number_re.match(self.file_content)
        if not result:
            return 1
        return result.group().count('\n') + 1

    def get_valid_tokens(self):
        """Return a generator with all tokens which we should care
        to look for the tasks"""

        line = self._get_initial_line_number()

        for token in self.lexer.get_tokens(self.file_content):
            text = token[1]
            if '\n' in text:
                line += 1

            if token[0] is Token.Comment:
                yield {'token': token[0], 'text': text,
                       'line_number': line}

    def get_tasks(self):
        """Return a generator with Task instances"""
        for token in self.get_valid_tokens():
            task = Task(token['text'])
            task.filepath = self.filepath
            task.line_number = token['line_number']
            yield task


class Task:
    """ One day, this will be the django model """

    def __init__(self, text):
        self.text = text

    text = ''
    assigned = None
    commit = None
    filepath = ''
    line = 0
    repository = None
    closed = False
    creation_time = ''
