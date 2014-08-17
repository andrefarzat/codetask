
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
