import re


class BaseParser:
    pattern = re.compile(r'\.txt$')

    def __init__(self, text):
        self.text = self.remove_markers(text)

    @classmethod
    def file_matches(self, filepath):
        if self.pattern.match(filepath):
            return True
        else:
            return False

    def remove_markers(self, text):
        raise NotImplementedError()


class PythonParser(BaseParser):
    pattern = re.compile(r'\.py$')

    def remove_markers(self, text):
        if text.startswith('#'):
            return text[1:]
        else:
            return text[3:-3]


PARSERS = (PythonParser, )


def get_parser_for_filename(filename):
    for parser in PARSERS:
        if parser.file_matches(filename):
            return parser
    return None
