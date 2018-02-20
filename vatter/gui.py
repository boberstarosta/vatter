import tkinter as tk
from . import settings


class MainWindow(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.option_add('*Font', 'times 14')

        ti = TextInput(self, min_length=3, max_length=10)
        ti.pack(padx=4, pady=4)

        fi = FloatInput(self, min_value=-10, max_value=1000000)
        fi.pack(padx=4, pady=4)

        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())


class TextInput(tk.Entry):
    def __init__(self, parent, min_length=None, max_length=None):
        self.var = tk.StringVar()
        super().__init__(parent, textvariable=self.var, **settings.INPUT_STYLE)

        if min_length is not None and max_length is not None:
            assert min_length < max_length, 'min_length must be smaller than max_length'
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


class FloatInput(TextInput):
    def __init__(self, parent, min_value=None, max_value=None):
        super().__init__(parent)

        if min_value is not None and max_value is not None:
            assert min_value < max_value, 'min_value must be smaller than max_value'
        self.min_value = min_value
        self.max_value = max_value

    def is_valid(self):
        value = self.value
        if value is None:
            return False
        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False

        return super().is_valid()

    @property
    def value(self):
        try:
            return float(self.text.replace(',', '.'))
        except ValueError:
            return None

    @value.setter
    def value(self, value):
        self.text = settings.FLOAT_FORMAT_STRING.format(value)
