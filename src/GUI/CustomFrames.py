import tkinter as tk
from .CustomWidgets import MarkdownEditor


class ManagePage(tk.Frame):
    def __init__(self, parent, colours, state, button_styles, fnt_main, *args, **kwargs):
        self.colours = colours
        self.button_styles = button_styles
        self.fnt_main = fnt_main
        self.state = state
        tk.Frame.__init__(self,
                          master=parent,
                          width=800,
                          height=800,
                          background=self.colours["main"], *args, **kwargs)

        # Left hand side

        self.frm_fldexp = tk.Frame(master=self,
                                   background=self.colours["border"],
                                   )
        self.frm_fldexp.pack(fill=tk.Y, side=tk.LEFT, expand=False)

        self.lb_folders = tk.Listbox(
            master=self.frm_fldexp,
            background=self.colours["border"],
            font=self.fnt_main,
            foreground=self.colours["text"],
        )
        self.lb_folders.bind('<<ListboxSelect>>', self.on_select)
        self.fill_folders()
        self.lb_folders.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.frm_fldbtns = tk.Frame(master=self.frm_fldexp)
        self.frm_fldbtns.rowconfigure(0, weight=1)
        self.frm_fldbtns.columnconfigure(1, weight=1)
        self.frm_fldbtns.pack(fill=tk.X, side=tk.TOP, expand=False)

        self.btn_newarea = tk.Button(master=self.frm_fldbtns,
                                     text="New Area",
                                     command="",
                                     **self.button_styles)
        self.btn_newarea.grid(row=1, column=0, sticky="ew")

        self.btn_newfolder = tk.Button(master=self.frm_fldbtns,
                                       text="Add Folder",
                                       command="",
                                       **self.button_styles)
        self.btn_newfolder.grid(row=1, column=1, sticky="ew")

        # Right hand side

        self.frm_fldmng = tk.Frame(master=self,
                                   background=self.colours["main"]
                                   )
        self.frm_fldmng.columnconfigure(0, weight=1)
        self.frm_fldmng.columnconfigure(1, weight=1)
        self.frm_fldmng.columnconfigure(2, weight=1)
        self.frm_fldmng.rowconfigure(0, weight=1)
        self.frm_fldmng.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.frm_foldertags = tk.Frame(
            master=self.frm_fldmng,
            background=self.colours["main"],
            borderwidth=1,
            relief=tk.RIDGE,
        )
        self.frm_foldertags.grid(row=0, column=0, sticky="nsew")

        self.frm_fldinfo = tk.Frame(
            master=self.frm_fldmng,
            background=self.colours["main"],
            borderwidth=1,
            relief=tk.RIDGE,
        )
        self.frm_fldinfo.grid(row=0, column=2, sticky="nsew")

        self.frm_files = tk.Frame(
            master=self.frm_fldmng,
            background=self.colours["main"],
            borderwidth=1,
            relief=tk.RIDGE,
        )
        self.frm_files.grid(row=0, column=1, sticky="nsew")

        self.grid(row=0, column=0, sticky="nsew")

    def fill_folders(self):
        self.lb_folders.delete(0, tk.END)
        if self.state.current_area is not None:
            for folder in self.state.manager.get_folders(self.state.current_area):
                self.lb_folders.insert(tk.END, folder)

    def on_select(self, event):
        widget = event.widget
        index = widget.curselection()[0]
        folder = widget.get(index)
        self.fill_folder_info(folder=folder)
        self.fill_tags(folder=folder)
        self.fill_files(folder=folder)

    def fill_tags(self, folder):
        data = self.state.manager.get_folder_info(area=self.state.current_area, folder=folder)
        for widget in self.frm_foldertags.winfo_children():
            widget.destroy()
        if data is not None:
            for tag in data["tags"]:
                frm_label = tk.Frame(master=self.frm_foldertags,
                                     background=self.colours["main"],
                                     relief=tk.RIDGE
                                     )
                frm_label.pack(fill=tk.X, side=tk.TOP, expand=False)
                label = tk.Label(
                    master=frm_label,
                    text=tag,
                    background=self.colours["main"],
                    foreground=self.colours["text"],
                    font=self.fnt_main,
                )
                label.pack(fill=tk.Y, side=tk.LEFT, expand=False)

                btn = tk.Button(
                    master=frm_label,
                    text="Remove",
                    **self.button_styles,
                    command=lambda: self.remove_tag(folder=folder, tag=tag),
                )
                btn.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

    def fill_folder_info(self, folder):
        data = self.state.manager.get_folder_info(area=self.state.current_area, folder=folder)
        for widget in self.frm_fldinfo.winfo_children():
            widget.destroy()
        if data is not None:
            for type, value in data.items():
                if type == "tags":
                    continue
                else:
                    frm_label = tk.Frame(master=self.frm_fldinfo,
                                         background=self.colours["main"],
                                         relief=tk.RIDGE
                                         )
                    frm_label.pack(fill=tk.X, side=tk.TOP, expand=False)
                    lbl_type = tk.Label(
                        master=frm_label,
                        text=type,
                        background=self.colours["main"],
                        foreground=self.colours["text"],
                        font=self.fnt_main,
                    )
                    lbl_type.pack(fill=tk.Y, side=tk.LEFT, expand=False)

                    lbl_value = tk.Label(
                        master=frm_label,
                        text=value,
                        background=self.colours["main"],
                        foreground=self.colours["text"],
                        font=self.fnt_main,
                    )
                    lbl_value.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

    def fill_files(self, folder):
        for widget in self.frm_files.winfo_children():
            widget.destroy()
        for file in self.state.manager.get_files(area=self.state.current_area, folder=folder):
            frm_file = tk.Frame(
                master=self.frm_files,
                background=self.colours["main"],
                relief=tk.RIDGE
            )
            frm_file.pack(fill=tk.X, side=tk.TOP, expand=False)
            lbl_file = tk.Label(
                master=frm_file,
                text=file,
                background=self.colours["main"],
                foreground=self.colours["text"],
                font=self.fnt_main,
            )
            lbl_file.pack(fill=tk.Y, side=tk.LEFT, expand=False)
            btn_load = tk.Button(
                master=frm_file,
                text="Open",
                **self.button_styles,
                command=""
            )
            btn_load.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

    def remove_tag(self, folder, tag):
        self.state.manager.remove_tag(area=self.state.current_area, folder=folder, tag=tag)
        self.fill_folder_info(folder=folder)


class EditPage(tk.Frame):
    def __init__(self, parent, colours, state, button_styles, fnt_main, *args, **kwargs):
        self.colours = colours
        self.button_styles = button_styles
        self.fnt_main = fnt_main
        self.state = state
        tk.Frame.__init__(self,
                          master=parent,
                          width=800,
                          height=800,
                          background=self.colours["main"], *args, **kwargs)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        frm_buttons = tk.Frame(master=self,
                               background=self.colours["border"],
                               highlightthickness=1,
                               relief=tk.RIDGE,
                               )
        frm_buttons.grid(row=0, column=0, sticky="ns", )
        btn_save = tk.Button(master=frm_buttons, text="Save",
                             **self.button_styles
                             )
        btn_save.pack(fill=tk.X, side=tk.TOP, expand=False)

        btn_saveas = tk.Button(master=frm_buttons, text="New Save",
                               **self.button_styles
                               )
        btn_saveas.pack(fill=tk.X, side=tk.TOP, expand=False)

        frm_textarea = tk.Frame(master=self,
                                background=self.colours["main"],
                                )
        frm_textarea.grid(row=0, column=1, sticky="nsew")

        txt_area = MarkdownEditor(master=frm_textarea,
                                  background=self.colours["main"],
                                  foreground=self.colours["text"],
                                  font=self.fnt_main,
                                  borderwidth=1,
                                  relief=tk.SUNKEN,
                                  padx=5,
                                  pady=5,
                                  )
        txt_area.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        vsb_area = tk.Scrollbar(
            master=frm_textarea,
            orient="vertical",
            borderwidth=1,
            command=txt_area.yview)
        vsb_area.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        txt_area.configure(yscrollcommand=vsb_area.set)

        self.grid(row=0, column=0, sticky="nsew")
