import tkinter as tk
import threading
from .MainFrame import MainLayout


class GraphicalUserInterface(tk.Tk, threading.Thread):
    def __init__(self, manager, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        tk.Tk.__init__(self, *args, **kwargs)
        self.minsize(710, 470)
        self.manager = manager
        self.current_frame = None

        self.data = {
            "manager": manager,
            "current_area": None,
        }

        self.current_frame = MainLayout(parent=self, controller=self, data=self.data)
        self.current_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.title("NoteManager")

    def run(self):
        self.mainloop()
