import os
import re
from pygments.lexers import get_lexer_for_filename, ClassNotFound
from pygments.token import Token

from codetask.parsers import get_parser_for_filename


VALID_COMMENT_TOKENS = [Token.Comment, Token.Comment.Single]


class DirExtractor:
    """Extractor which acts in a given dir"""

    def __init__(self, path):
        if not os.path.isdir(path):
            raise ValueError('%s is not a directory' % path)

        self.path = path

    def get_all_files(self):
        """Returns a generator with all files with the abs path"""
        for root, dirs, files in os.walk(self.path):
            for filename in files:
                yield os.path.join(root, filename)

    def get_extractors(self):
        """Returns a generator with all extractor instances
        for all valid files"""
        for filepath in self.get_all_files():
            try:
                lexer = get_lexer_for_filename(filepath)
            except ClassNotFound:
                continue

            yield Extractor(filepath, lexer=lexer)


class Extractor:
    """Does the extration in one single file"""

    _initial_line_number_re = re.compile(r'^(\n+)')

    def __init__(self, filepath, lexer=None):
        if not os.path.isfile(filepath):
            raise ValueError("%s does not exist" % filepath)

        self.filepath = filepath
        self.lexer = lexer or get_lexer_for_filename(filepath)

    def __repr__(self):
        return '<Extractor filepath=%s>' % self.filepath

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

            if token[0] in VALID_COMMENT_TOKENS:
                yield {'token': token[0], 'text': text,
                       'line_number': line}

    def get_tasks(self):
        """Return a generator with ExtractedTask instances"""
        for token in self.get_valid_tokens():
            task = ExtractedTask(text=token['text'], filepath=self.filepath,
                                 line_number=token['line_number'])
            yield task


class ExtractedTask:
    """Default scaffolding for an extracted task"""

    def __init__(self, text, filepath, line_number=None):
        Parser = get_parser_for_filename(filepath)
        parser = Parser(text)

        self.raw_text = text
        self.text = parser.text.strip()
        self.filepath = filepath
        self.line_number = line_number
        self.username = parser.username
        self.label = parser.label

    def __repr__(self):
        text = ('text="%s"' % self.text[:30]) if self.text else ''
        label = ('label="%s" ' % self.label) if self.label else ''
        return '<ExtractedTask {label}{text}>'.format(text=text, label=label)

    def is_valid(self):
        return self.text != ''
