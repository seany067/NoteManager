import tkinter as tk
import os
import enchant


'''
This class will override the text area so that it can use spellcheckers and potentially a md linter
'''
class MarkdownEditor(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.tag_configure("misspelled", foreground="red", underline=True)
        self.bind("<space>", self.spellcheck)
        self.bind("<R eturn>", self.spellcheck)
        self.checker = enchant.Dict("en_GB")

        with open(os.path.join(os.getcwd(), "src/GUI", "words_alpha.txt"), 'r') as f:
            self.dictionary = set(f.read().split('\n'))

    def spellcheck(self, event):
        wordend = self.index("insert")
        wordstart = self.index("{0} wordstart".format(self.index(wordend+"-1c")))
        word = self.get(wordstart, wordend)
        print(word, wordstart, wordend)
        if word in self.dictionary:
            print(f"Correct spelling: {word}")
            self.tag_remove("misspelled", wordstart, "%s+%dc" % (wordstart, len(word)))
        else:
            print(f"incorrect spelling: {word}")
            self.tag_add("misspelled", wordstart, "%s+%dc" % (wordstart, len(word)))
