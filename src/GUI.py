import tkinter as tk
import threading


class EditorPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        frm_menubar = tk.Frame(master=parent)
        btn_text1 = tk.Button(master=frm_menubar, text="text1")
        btn_text1.pack(fill=tk.X, side=tk.LEFT, expand=True)
        btn_text2 = tk.Button(master=frm_menubar, text="text2")
        btn_text2.pack(fill=tk.X, side=tk.LEFT, expand=True)
        btn_text3 = tk.Button(master=frm_menubar, text="text3")
        btn_text3.pack(fill=tk.X, side=tk.LEFT, expand=True)
        btn_text4 = tk.Button(master=frm_menubar, text="text4")
        btn_text4.pack(fill=tk.X, side=tk.LEFT, expand=True)

        frm_main = tk.Frame(master=parent, width=800, height=800, bg="blue")
        frm_main.rowconfigure(0, weight=1)
        frm_main.columnconfigure(1, weight=1)

        frm_buttons = tk.Frame(master=frm_main, bg="red")
        btn_save = tk.Button(master=frm_buttons, text="Save")
        btn_save.grid(row=0, column=0, sticky="ew")
        frm_buttons.grid(row=0, column=0, sticky="ns")

        txt_area = tk.Text(master=frm_main)
        txt_area.grid(row=0, column=1, sticky="nsew")

        frm_menubar.pack(fill=tk.X, side=tk.TOP, expand=False)
        frm_main.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


class GraphicalUserInterface(tk.Tk):
    def __init__(self, manager, *args, **kwargs):
        self.manager = manager
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(master=self)
        container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        EditorPage(parent=container, controller=self).tkraise()

    def create_editor(self):
        pass

    def save_contents(self, event):
        pass
        # text = self.widgets["txt_mainarea"]["object"].get("1.0", tk.END)

    def run(self):
        self.mainloop()


class GUIThread(threading.Thread):
    def __init__(self, manager):
        self.window = GraphicalUserInterface(manager=manager)
        self.manager = manager
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.window.mainloop()



