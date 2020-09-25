from src import *
import sys

manager = DirectoryManager()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Opening GUI app...")
        gui = GraphicalUserInterface(manager=manager)
        gui.mainloop()
    else:
        print("Starting CLI app...")
        parser = CommandLineInterface()
        parser.parse(manager=manager)
