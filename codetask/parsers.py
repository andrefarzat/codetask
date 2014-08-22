import re


class BaseParser:
    pattern = re.compile(r'\w+\.txt$')
    _squared_pattern = re.compile(r'(\[.?\])(\([\w\s\-\.\@]+\))?:?(.+)?$')
    _colon_pattern = re.compile(r'(\w+):([\w\s]+)?')
    _username_pattern = re.compile(r'(^\(|\)$)')

    def __init__(self, text):
        self._text = self.remove_markers(text)
        self.closed = False
        self.username = ''
        self.text = ''
        self.label = ''
        self.parse_text(text)

    @classmethod
    def file_matches(self, filepath):
        if self.pattern.match(filepath):
            return True
        else:
            return False

    def remove_markers(self, text):
        return text.strip()

    def parse_text(self, text):
        if text.startswith('['):
            self._parse_squared_text(text)

    def parse_username(self, username):
        username = username.strip()
        username = self._username_pattern.sub('', username)
        return username.strip()

    def _parse_squared_text(self, text):
        result = self._squared_pattern.match(text)
        if result:
            self.closed = (result.group(1) == '[x]')
            self.username = self.parse_username(result.group(2) or '')
            self.text = (result.group(3) or '').strip()
            self.label = ''

    def _parse_colon_text(self, text):
        result = self._colon_pattern.match(text)
        if result:
            self.closed = False
            self.username = (result.group(2) or '').strip()
            self.text = (result.group(3) or '').strip()
            self.label = ''


class PythonParser(BaseParser):
    pattern = re.compile(r'\w+\.py$')

    def remove_markers(self, text):
        if text.startswith('#'):
            return text[1:].strip()
        else:
            return text[3:-3].strip()


PARSERS = (PythonParser, )


def get_parser_for_filename(filename):
    for parser in PARSERS:
        if parser.file_matches(filename):
            return parser
    return None
