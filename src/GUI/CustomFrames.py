import tkinter as tk
from .CustomWidgets import MarkdownEditor


class ManagePage(tk.Frame):
    def __init__(self, parent, colours, data, button_styles, fnt_main, *args, **kwargs):
        self.colours = colours
        self.data = data
        self.button_styles = button_styles
        self.fnt_main = fnt_main
        tk.Frame.__init__(self,
                          master=parent,
                          width=800,
                          height=800,
                          background=self.colours["main"], *args, **kwargs)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.lb_folders = tk.Listbox(
            master=self,
        )
        self.fill_folders()
        self.lb_folders.grid(row=0, column=0, sticky="nsew")
        self.lbl_text2 = tk.Label(
            master=self,
            text="Hello there",
        )
        self.lbl_text2.grid(row=0, column=1, sticky="nsew")

        self.grid(row=0, column=0, sticky="nsew")

    def fill_folders(self):
        self.lb_folders.delete(0, tk.END)
        if self.data["current_area"] is not None:
            for folder in self.data["manager"].get_folders(self.data["current_area"]):
                self.lb_folders.insert(tk.END, folder)


class EditPage(tk.Frame):
    def __init__(self, parent, colours, data, button_styles, fnt_main, *args, **kwargs):
        self.colours = colours
        self.data = data
        self.button_styles = button_styles
        self.fnt_main = fnt_main
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
        btn_save = tk.Button(master=frm_buttons, text="Save",
                             **self.button_styles
                             )
        btn_save.grid(row=0, column=0, sticky="ew")
        frm_buttons.grid(row=0, column=0, sticky="ns", )

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
