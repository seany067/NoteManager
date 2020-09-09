from src import *
import sys

manager = DirectoryManager()
guithread = None

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Opening GUI app...")

        gui = GraphicalUserInterface(manager=manager)
        gui.run()

    else:
        print("Starting CLI app...")
        parser = CommandLineInterface()
        parser.parse(manager=manager)

    if guithread is not None:
        guithread.join()
