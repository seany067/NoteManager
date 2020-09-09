import tkinter as tk


'''
This class will override the text area so that it can use spellcheckers and potentially a md linter
'''
class MarkdownEditor(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
