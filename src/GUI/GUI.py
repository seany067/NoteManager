import tkinter as tk
import threading
from .MainFrame import MainLayout
from ..State import State


class GraphicalUserInterface(tk.Tk, threading.Thread):
    def __init__(self, manager, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(720, 480)
        self.state = State()
        self.current_frame = MainLayout(parent=self, controller=self, state=self.state)
        self.current_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.title("NoteManager")

    def run(self):
        self.mainloop()
