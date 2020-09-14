from .Directories import DirectoryManager


class State(object):
    def __init__(self):
        self.manager = DirectoryManager()
        self.current_area = None
        self.current_folder = None
        self.current_file = None
