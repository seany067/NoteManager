import tkinter as tk
from tkinter import messagebox
from .CustomWidgets import MarkdownEditor
import copy


class ManagePage(tk.Frame):
    def __init__(self, parent, mainframe, colours, state, button_styles, fnt_main, *args, **kwargs):
        self.colours = colours
        self.button_styles = button_styles
        self.fnt_main = fnt_main
        self.state = state
        self.parent = parent
        self.mainframe = mainframe
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

        frm_fldbtns = tk.Frame(master=self.frm_fldexp)
        frm_fldbtns.rowconfigure(0, weight=1)
        frm_fldbtns.columnconfigure(1, weight=1)
        frm_fldbtns.pack(fill=tk.X, side=tk.TOP, expand=False)

        btn_newarea = tk.Button(master=frm_fldbtns,
                                text="New Area",
                                command="",
                                **self.button_styles)
        btn_newarea.grid(row=1, column=0, sticky="ew")

        btn_newfolder = tk.Button(master=frm_fldbtns,
                                  text="Add Folder",
                                  command="",
                                  **self.button_styles)
        btn_newfolder.grid(row=1, column=1, sticky="ew")

        # Right hand side

        frm_fldmng = tk.Frame(master=self,
                              background=self.colours["main"]
                              )
        frm_fldmng.columnconfigure(0, weight=1)
        frm_fldmng.columnconfigure(1, weight=1)
        frm_fldmng.columnconfigure(2, weight=1)
        frm_fldmng.rowconfigure(0, weight=1)
        frm_fldmng.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        self.frm_foldertags = tk.Frame(
            master=frm_fldmng,
            background=self.colours["main"],
            borderwidth=1,
            relief=tk.RIDGE,
        )
        self.frm_foldertags.grid(row=0, column=0, sticky="nsew")

        self.frm_fldinfo = tk.Frame(
            master=frm_fldmng,
            background=self.colours["main"],
            borderwidth=1,
            relief=tk.RIDGE,
        )
        self.frm_fldinfo.grid(row=0, column=2, sticky="nsew")

        self.frm_files = tk.Frame(
            master=frm_fldmng,
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

            btn_newtag = tk.Button(
                master=self.frm_foldertags,
                text="Add tag",
                **self.button_styles,
                command=lambda folder=folder: self.add_tag(folder=folder)
            )
            btn_newtag.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

    def fill_folder_info(self, folder):
        data = self.state.manager.get_folder_info(area=self.state.current_area, folder=folder)
        for widget in self.frm_fldinfo.winfo_children():
            widget.destroy()
        if data is not None:
            for type, value in data.items():
                if type == "tags":
                    continue
                else:
                    frm_label = tk.Frame(
                        master=self.frm_fldinfo,
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

    def open_file(self, folder, file):
        print(file)
        self.mainframe.open_file(area=self.state.current_area, folder=folder, file=file)

    def fill_files(self, folder):
        for widget in self.frm_files.winfo_children():
            widget.destroy()
        files = self.state.manager.get_files(area=self.state.current_area, folder=folder)[:]
        for i in range(0, len(self.state.manager.get_files(area=self.state.current_area, folder=folder)[:])):
            filename = files[i]
            foldername = copy.deepcopy(folder)

            frm_file = tk.Frame(
                master=self.frm_files,
                background=self.colours["main"],
                relief=tk.RIDGE
            )
            frm_file.pack(fill=tk.X, side=tk.TOP, expand=False)
            lbl_file = tk.Label(
                master=frm_file,
                text=filename,
                background=self.colours["main"],
                foreground=self.colours["text"],
                font=self.fnt_main,
            )

            lbl_file.pack(fill=tk.Y, side=tk.LEFT, expand=False)
            btn_load = tk.Button(
                master=frm_file,
                text="Open",
                **self.button_styles,
                command=lambda filename=filename, foldername=foldername: self.open_file(file=filename,
                                                                                        folder=foldername),
            )
            btn_load.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

    def remove_tag(self, folder, tag):
        self.state.manager.remove_tag(area=self.state.current_area, folder=folder, tag=tag)
        self.fill_folder_info(folder=folder)

    def add_tag(self, folder):
        tag = self.new_tag_popup_window()
        if tag is not None:
            self.state.manager.add_tags(area=self.state.current_area, folder=folder, tags=tag)
            self.fill_folder_info(folder=folder)

    def new_tag_popup_window(self):
        window = tk.Toplevel()
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.geometry("250x100")
        window.title("New Tag")
        window.configure(background=self.colours["main"])
        # window.grab_set()

        lbl_filename = tk.Label(
            master=window,
            text="Tag:",
            background=self.colours["main"],
            foreground=self.colours["text"],
            font=self.fnt_main,
        )
        lbl_filename.grid(row=0, column=0, sticky="e")

        data = tk.StringVar()
        ent_tag = tk.Entry(
            master=window,
            font=self.fnt_main,
            background=self.colours["main"],
            foreground=self.colours["text"],
            textvariable=data
        )
        ent_tag.grid(row=0, column=1, sticky="w")

        btn_cancel = tk.Button(
            master=window,
            **self.button_styles,
            text="Cancel",
            command=window.destroy,
        )
        btn_cancel.grid(row=1, column=0, sticky="e")

        btn_add = tk.Button(
            master=window,
            **self.button_styles,
            text="Add Tag",
            command=window.destroy
        )
        btn_add.grid(row=1, column=1, sticky="w")

        window.wait_window()
        return data.get()


class EditPage(tk.Frame):
    def __init__(self, parent, mainframe, colours, state, button_styles, fnt_main, *args, **kwargs):
        self.colours = colours
        self.button_styles = button_styles
        self.fnt_main = fnt_main
        self.state = state
        self.mainframe = mainframe
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

        frm_textarea = tk.Frame(master=self,
                                background=self.colours["main"],
                                )
        frm_textarea.grid(row=0, column=1, sticky="nsew")

        self.txt_area = MarkdownEditor(
            master=frm_textarea,
            background=self.colours["main"],
            foreground=self.colours["text"],
            font=self.fnt_main,
            borderwidth=1,
            relief=tk.SUNKEN,
            padx=5,
            pady=5,
        )
        self.txt_area.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        vsb_area = tk.Scrollbar(
            master=frm_textarea,
            orient="vertical",
            borderwidth=1,
            command=self.txt_area.yview)
        vsb_area.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
        self.txt_area.configure(yscrollcommand=vsb_area.set)

        btn_save = tk.Button(
            master=frm_buttons,
            text="Save",
            **self.button_styles,
            command=lambda data=self.txt_area.get("1.0", tk.END): self.quick_save_file(data=data)
        )
        btn_save.pack(fill=tk.X, side=tk.TOP, expand=False)

        btn_saveas = tk.Button(
            master=frm_buttons,
            text="New Save",
            **self.button_styles,
            command=self.save_as_pop,
        )
        btn_saveas.pack(fill=tk.X, side=tk.TOP, expand=False)

        self.grid(row=0, column=0, sticky="nsew")

    def save_as_pop(self):
        window = tk.Toplevel()
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(1, weight=1)
        window.geometry("250x100")
        window.title("Save As")
        window.configure(background=self.colours["main"])
        window.grab_set()

        lbl_filename = tk.Label(
            master=window,
            text="Filename:",
            background=self.colours["main"],
            foreground=self.colours["text"],
            font=self.fnt_main,
        )
        lbl_filename.grid(row=0, column=0, sticky="e")

        ent_filename = tk.Entry(
            master=window,
            font=self.fnt_main,
            background=self.colours["main"],
            foreground=self.colours["text"],
        )
        ent_filename.grid(row=0, column=1, sticky="w")

        btn_cancel = tk.Button(
            master=window,
            **self.button_styles,
            text="Cancel",
            command=window.destroy,
        )
        btn_cancel.grid(row=1, column=0, sticky="e")

        def save_button():
            self.new_save_file(name=ent_filename.get(), data=self.txt_area.get("1.0", tk.END))
            window.destroy()

        btn_cancel = tk.Button(
            master=window,
            **self.button_styles,
            text="Save",
            command=save_button,
        )
        btn_cancel.grid(row=1, column=1, sticky="w")

    def new_save_file(self, data, name):
        # Save file to folder
        if self.state.current_area is None:
            tk.messagebox.showerror(title="Error", message="Please select an area first")
            return
        outcome = self.state.manager.new_save_file(
            area=self.state.current_area,
            filename=name,
            filecontent=data
        )
        if outcome[0]:
            tk.messagebox.showinfo(title="Success", message=outcome[1])
            self.state.current_file = outcome[2]
            self.state.current_folder = outcome[3]
        else:
            tk.messagebox.showerror(title="Error", message=outcome[1])

    def quick_save_file(self, data):
        # Update currently open file
        if self.state.current_area is None:
            tk.messagebox.showerror(title="Error", message="Please select an area first")
            return
        if self.state.current_file is None:
            return self.save_as_pop()
        outcome = self.state.manager.save_file(
            area=self.state.current_area,
            folder=self.state.current_folder,
            filename=self.state.current_file,
            filecontent=data
        )
        if outcome[0]:
            tk.messagebox.showinfo(title="Success", message=outcome[1])
            self.state.current_file = outcome[2]
            self.state.current_folder = outcome[3]
        else:
            tk.messagebox.showerror(title="Error", message=outcome[1])

    def manual_save_file(self, data):
        # Manually save the file using the windows file explorer
        pass

    def check_save(self, data):
        return self.state.manager.check_save(area=self.state.current_area, folder=self.state.current_folder,
                                             file=self.state.current_file, data=data)

    def open_file(self, area, folder, file):
        if self.state.current_file and not self.check_save(data=self.txt_area.get("1.0", tk.END)):
            result = tk.messagebox.askyesnocancel("Save", "Would you like to save changes to the currently open file?")
            if result:
                self.quick_save_file(data=self.txt_area.get("1.0", tk.END))
            elif result is None:
                return
        data = self.state.manager.get_file_content(area, folder, file)
        self.txt_area.delete("1.0", tk.END)
        self.txt_area.insert("1.0", data)
        self.state.current_folder = folder
        self.state.current_file = file
