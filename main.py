from src import *
import sys

manager = DirectoryManager()

if __name__ == '__main__':
    if not len(sys.argv):
        # Launch Tkinter app
        pass
    else:
        parser = CommandLineInterface()
        parser.parse(manager=manager)
