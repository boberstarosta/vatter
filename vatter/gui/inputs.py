import tkinter as tk
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

        self.bind('<Escape>', lambda e: self.master.focus_set())

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


class ModelChoiceInput(tk.Frame):
    def __init__(self, parent, model, filter_fields):
        super().__init__(parent)

        self.var = tk.StringVar()
        self.model = model
        self.filter_fields = filter_fields
        self.session = db.Session()
        self.objects = {}

        self.entry_widget = tk.Entry(self, textvariable=self.var, **settings.INPUT_STYLE)
        self.entry_widget.pack(side=tk.TOP, expand=True, fill=tk.X)

        self.listbox_widget = tk.Listbox(self, **settings.INPUT_STYLE)
        self.listbox_widget.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        self.color_default = self.entry_widget.cget('background')
        self.color_error = '#ff9999'
        self.color_ok = '#b3ff99'

        self.entry_widget.bind('<KeyRelease>', self.update_autocomplete)
        self.entry_widget.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry_widget.bind('<FocusOut>', self.on_entry_focus_out)
        self.entry_widget.bind('<Down>', self.on_entry_down)
        self.entry_widget.bind('<Escape>', lambda e: self.master.focus_set())

        self.listbox_widget.bind('<FocusOut>', self.on_listbox_focus_out)
        self.listbox_widget.bind('<<ListboxSelect>>', self.on_listbox_select)
        self.listbox_widget.bind('<Return>', self.on_listbox_return)
        self.listbox_widget.bind('<KP_Enter>', self.on_listbox_return)
        self.listbox_widget.bind('<Escape>', self.on_listbox_escape)

        self.var.trace('w', self.update_background)

        self.update_autocomplete()
        self.listbox_widget.pack_forget()
        self.update_background()

    def get_queryset(self):
        text = '%' + self.var.get().strip() + '%'
        filter_clauses = [getattr(self.model, field).ilike(text) for field in self.filter_fields]
        return self.session.query(self.model).filter(or_(*filter_clauses)).all()

    def update_autocomplete(self, event=None):
        self.listbox_widget.delete(0, tk.END)
        self.objects.clear()
        self.listbox_widget['height'] = 5
        for record in self.get_queryset():
            self.listbox_widget.insert(tk.END, str(record))
            self.objects[str(record)] = record

    def on_entry_focus_in(self, event):
        self.listbox_widget.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

    def on_entry_focus_out(self, event):
        if self.focus_get() != self.listbox_widget:
            self.listbox_widget.pack_forget()

    def on_entry_down(self, event):
        self.listbox_widget.focus_set()
        self.listbox_widget.selection_set(0)
        self.listbox_widget.event_generate('<<ListboxSelect>>')

    def on_listbox_focus_out(self, event):
        if self.focus_get() != self.entry_widget:
            self.listbox_widget.pack_forget()

    def on_listbox_select(self, event):
        curselection = self.listbox_widget.curselection()
        if curselection:
            self.var.set(self.listbox_widget.get(curselection))

    def on_listbox_return(self, event):
        self.master.focus_set()
        self.listbox_widget.event_generate('<<ListboxSelect>>')

    def on_listbox_escape(self, event):
        self.entry_widget.focus_set()

    def get_selected_object(self):
        try:
            return self.objects[self.var.get()]
        except KeyError:
            return None

    def is_valid(self):
        return self.get_selected_object() is not None

    def update_background(self, *args):
        if self.is_valid():
            self.entry_widget.config(bg=self.color_ok)
        else:
            self.entry_widget.config(bg=self.color_error)
