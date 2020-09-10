import tkinter.filedialog
import tkinter as tk
import tkinter.font as tkFont
import os
from tkinter.messagebox import showwarning
from .CustomFrames import ManagePage, EditPage


class MainLayout(tk.Frame):
    colours = {
        "border": '#3B3B3B',
        "main": '#2B2B2B',
        "text": '#A9B7C6',
        "active": "#A6A6A6",
    }

    widgets = {
        "menubar": {},
        "statusbar": {},
        "editpage": {},
        "managepage": {},
    }

    frames = {}

    def __init__(self, parent, controller, state):
        self.fnt_main = tkFont.Font(root=controller, family="Arial", size=11)
        self.button_styles = {
            "background": self.colours["border"],
            "foreground": self.colours["text"],
            "activebackground": self.colours["active"],
            "font": self.fnt_main,
            "relief": tk.FLAT,
            "padx": 3,
            "pady": 1,
        }
        self.parent = parent
        self.controller = controller
        self.state = state
        tk.Frame.__init__(self, master=parent)

        self.content_frame = tk.Frame(
            master=self,
            background=self.colours["main"],
        )
        self.content_frame.rowconfigure(0, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

        self.build_menubar()
        self.build_pages()
        self.content_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.frames["editpage"].tkraise()
        self.build_statusbar()
        self.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

    def build_menubar(self):
        frm_menubar = tk.Frame(master=self,
                               background=self.colours["border"],
                               highlightthickness=1,
                               relief=tk.RIDGE,
                               )
        self.widgets["menubar"]["frm_menubar"] = frm_menubar

        btn_openarea = tk.Button(master=frm_menubar,
                                 text="Select area",
                                 command=self.browseFiles,
                                 **self.button_styles,
                                 )

        btn_openarea.pack(fill=tk.X, side=tk.LEFT, expand=False)
        self.widgets["menubar"]["btn_openarea"] = btn_openarea
        btn_manageframe = tk.Button(master=frm_menubar,
                                    text="Manage Areas",
                                    command=lambda: self.show_frame("managepage"),
                                    **self.button_styles,
                                    )
        self.widgets["menubar"]["btn_manageframe"] = btn_manageframe
        btn_manageframe.pack(fill=tk.X, side=tk.LEFT, expand=False)

        btn_texteditor = tk.Button(master=frm_menubar,
                                   text="Text Editor",
                                   command=lambda: self.show_frame("editpage"),
                                   **self.button_styles,
                                   )
        self.widgets["menubar"]["btn_texteditor"] = btn_texteditor
        btn_texteditor.pack(fill=tk.X, side=tk.LEFT, expand=False)

        frm_menubar.pack(fill=tk.X, side=tk.TOP, expand=False)

    def build_statusbar(self):
        frm_statusbar = tk.Frame(master=self,
                                 background=self.colours["border"],
                                 highlightthickness=1,
                                 relief=tk.RIDGE,
                                 )
        lbl_status = tk.Label(master=frm_statusbar,
                              text="Current Area: {}".format(self.state.current_area),
                              background=self.colours["border"],
                              foreground=self.colours["text"],
                              font=self.fnt_main
                              )
        self.widgets["statusbar"]["lbl_status"] = lbl_status
        lbl_status.grid(row=0, column=0, sticky="ens")
        frm_statusbar.pack(fill=tk.X, side=tk.TOP, expand=False)

    def build_pages(self):
        self.frames["editpage"] = EditPage(parent=self.content_frame,
                                           colours=self.colours,
                                           state=self.state,
                                           button_styles=self.button_styles,
                                           fnt_main=self.fnt_main)
        self.frames["managepage"] = ManagePage(parent=self.content_frame,
                                               colours=self.colours,
                                               state=self.state,
                                               button_styles=self.button_styles,
                                               fnt_main=self.fnt_main)

    def show_frame(self, framename):
        self.frames[framename].tkraise()

    def browseFiles(self):
        directory = tk.filedialog.askdirectory(
            initialdir="/",
            title="Select a File",
        )
        print(os.path.exists(os.path.join(directory, '.note_manager', 'settings.json')))
        if os.path.exists(os.path.join(directory, '.note_manager', 'settings.json')) and os.path.isfile(
                os.path.join(directory, '.note_manager', 'settings.json')):
            self.state.current_area = directory
            self.widgets["statusbar"]["lbl_status"].config(text=directory)
            self.frames["managepage"].fill_folders()
            return directory
        showwarning("Warning", "This area is not managed\nPlease select another")
        return None

# TODO: Will have to come back to this as it does not appear on the task bar after do this, so the app disappears

#     def build_windowsbar(self):
#         def move_window(event):
#             self.controller.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
#
#         self.controller.overrideredirect(True)  # turns off title bar, geometry
#
#         # make a frame for the title bar
#         title_bar = tk.Frame(master=self, bg='white', relief='raised', bd=2)
#
#         # put a close button on the title bar
#         close_button = tk.Button(title_bar, text='X', command=self.controller.destroy)
#
#         title_bar.pack(expand=1, fill=tk.X)
#         close_button.pack(side=tk.RIGHT)
#
#         # bind title bar motion to the move window function
#         title_bar.bind('<B1-Motion>', move_window)
