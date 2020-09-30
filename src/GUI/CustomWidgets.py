import tkinter as tk
import os
import enchant
import string


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
        self.checker = enchant.DictWithPWL("en_GB", os.path.join(os.getcwd(), "src/GUI", "accepted_words.txt"))

        with open(os.path.join(os.getcwd(), "src/GUI", "words_alpha.txt"), 'r') as f:
            self.dictionary = set(f.read().split('\n'))

    def spellcheck(self, event):
        wordend = self.index(tk.INSERT)
        wordstart = self.index("{0} wordstart".format(self.index(wordend + "-1c")))
        word = self.get(wordstart, wordend).strip().translate(str.maketrans('', '', string.punctuation))
        if not word:
            return
        print(word)
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
        word = self.get(wordstart, wordend).strip().translate(str.maketrans('', '', string.punctuation))
        if not word:
            return
        if not self.checker.check(word) and word != "\n":
            suggestions = self.checker.suggest(word)
            for w in suggestions:
                menu.add_command(
                    label=w,
                    command=lambda start=wordstart, end=wordend, newword=w: self.correct(start, end, newword)
                )
        menu.add_command(
            label="Add to Dictionary",
            command=lambda start=wordstart, end=wordend, word=word: self.add_to_dict(start, end, word)
        )
        menu.add_command(
            label="Ignore",
            command=lambda start=wordstart, end=wordend: self.ignore(start, end)
        )
        return menu

    def correct(self, start, end, word):
        self.delete(start, end)
        self.insert(start, word)

    def ignore(self, start, end):
        self.tag_remove("misspelled", start, end)

    def add_to_dict(self, start, end, word):
        self.checker.add(word)
        self.ignore(start, end)
