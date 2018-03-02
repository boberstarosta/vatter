import tkinter as tk
from tkinter import ttk
from sqlalchemy import or_
from .. import db, settings


class TextInput(tk.Entry):
    def __init__(self, parent, width=80, min_length=None, max_length=None):
        self.var = tk.StringVar()
        super().__init__(parent, textvariable=self.var, width=width, **settings.INPUT_STYLE)

        if min_length is not None and max_length is not None:
            assert min_length < max_length, 'min_length must be smaller than max_length'
        self.min_length = min_length
        self.max_length = max_length

        self.color_default = self.cget('background')
        self.color_error = '#ff9999'
        self.color_ok = '#b3ff99'

        self.var.trace('w', lambda *args: self.on_changed())
        self.on_changed()

    def on_changed(self):
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

    @property
    def value(self):
        return self.text
    @value.setter
    def value(self, value):
        self.text = value


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

        return True

    @property
    def value(self):
        try:
            return float(self.text.replace(',', '.').replace(' ', ''))
        except ValueError:
            return None

    @value.setter
    def value(self, value):
        self.text = settings.FLOAT_FORMAT_STRING.format(value)


class IntInput(TextInput):
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

        return True

    @property
    def value(self):
        try:
            return int(self.text)
        except ValueError:
            return None

    @value.setter
    def value(self, value):
        self.text = str(value)


class ModelChoiceInput(ttk.Combobox):
    def __init__(self, parent, model, filter_fields):
        self.var = tk.StringVar()
        super().__init__(parent, textvariable=self.var)
        self.model = model
        self.filter_fields = filter_fields
        self.session = db.Session()
        self.bind('<<ComboboxSelected>>', self.on_selected)
        self['values'] = self.get_queryset()
        self.var.trace('w', self.on_change)

    def get_queryset(self):
        filter = '%' + self.get() + '%'
        filter_conditions = [getattr(self.model, field).ilike(filter) for field in self.filter_fields]
        return self.session.query(self.model).filter(or_(*filter_conditions)).all()

    def on_change(self, *args):
        self['values'] = self.get_queryset()
        if self.focus:
            self.event_generate('<Down>')

    def on_selected(self, event):
        pass
