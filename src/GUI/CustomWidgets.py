import tkinter as tk
import os
import enchant


class MarkdownEditor(tk.Text):
    """
    This class will override the text area so that it can use spellcheckers and potentially a md linter
    """

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.tag_configure("misspelled", foreground="red", underline=True)
        self.bind("<space>", self.spellcheck)
        self.bind("<Return>", self.spellcheck)
        self.bind("<Button-3>", self.show_popup)
        self.checker = enchant.Dict("en_GB")

        with open(os.path.join(os.getcwd(), "src/GUI", "words_alpha.txt"), 'r') as f:
            self.dictionary = set(f.read().split('\n'))

    def spellcheck(self, event):
        wordend = self.index(tk.INSERT)
        wordstart = self.index("{0} wordstart".format(self.index(wordend + "-1c")))
        word = self.get(wordstart, wordend)
        if self.checker.check(word):
            self.tag_remove("misspelled", wordstart, "%s+%dc" % (wordstart, len(word)))
        else:
            self.tag_add("misspelled", wordstart, "%s+%dc" % (wordstart, len(word)))

    def show_popup(self, event):
        menu = self.create_popup(event.x_root, event.y_root)
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    def create_popup(self, x, y):
        menu = tk.Menu(self,
                       tearoff=0,
                       )
        pos = self.index(f"@{x - self.winfo_rootx()},{y - self.winfo_rooty()}")
        self.mark_set(tk.INSERT, pos)
        wordstart = self.index(f"{pos} wordstart")
        wordend = self.index(f"{pos} wordend")
        word = self.get(wordstart, wordend)
        if not self.checker.check(word) and word != "\n":
            suggestions = self.checker.suggest(word)
            for w in suggestions:
                menu.add_command(
                    label=w,
                    command=lambda start=wordstart, end=wordend, newword=w: self.correct(start, end, newword)
                )
        return menu

    def correct(self, start, end, word):
        self.delete(start, end)
        self.insert(start, word)
