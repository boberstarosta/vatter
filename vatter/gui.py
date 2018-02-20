from tkinter import *
from . import settings


#default_font = tkFont.nametofont("TkDefaultFont")
#default_font.configure(size=48)


class MainWindow(Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        i = TextInput(self, min_length=3, max_length=10)
        i.pack(padx=4, pady=4)

        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())


class TextInput(Entry):
    def __init__(self, parent, min_length=None, max_length=None):
        self.var = StringVar()
        super().__init__(parent, textvariable=self.var, **settings.INPUT_STYLE)

        self.min_length = min_length
        self.max_length = max_length

        self.color_default = self.cget("background")
        self.color_error = "#ff9999"
        self.color_ok = "#b3ff99"

        self.var.trace("w", self.on_changed)
        self.on_changed()

    def on_changed(self, *args):
        if self.is_valid():
            self.config(bg=self.color_ok)
        else:
            self.config(bg=self.color_error)

    def is_valid(self):
        length = len(self.var.get())
        if self.min_length is not None and length < self.min_length:
            return False
        if self.max_length is not None and length > self.max_length:
            return False
        return True

    @property
    def text(self):
        return self.var.get()

    @text.setter
    def text(self, value):
        self.var.set(value)
