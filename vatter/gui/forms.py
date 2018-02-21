import tkinter as tk
from . import inputs, settings
from .. import db, models


class Field:
    def __init__(self, column_name, caption=None, widget_class=None, **widget_args):
        self.column_name = column_name
        self.caption = caption
        self.widget_class = widget_class
        self.widget_args = widget_args


class Form(tk.Toplevel):
    fields = []

    def __init__(self, parent, obj, **kwargs):
        super().__init__(parent, **kwargs)

        self.session = db.Session()
        self.obj = self.session.merge(obj)

        frame = tk.Frame(self)
        frame.pack(fill='both', expand=True)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.widgets = []

        for i, field in enumerate(self.fields):
            frame.grid_rowconfigure(i, weight=1)
            tk.Label(frame, text=field.caption + ':').grid(column=0, row=i, sticky='ew', **settings.GRID_STYLE)
            widget = field.widget_class(frame, **field.widget_args)
            widget.grid(column=1, row=i, sticky='ew', **settings.GRID_STYLE)
            self.widgets.append(widget)
            widget.var.trace('w', lambda *args, f=field, w=widget: self.on_change(f, w))

        frame = tk.Frame(self)
        frame.pack(side='bottom', fill='x', expand=True)
        tk.Button(frame, text='Zapisz', command=self.save).pack(**settings.PACK_STYLE)

        self.bind('<Return>', lambda *args: self.save())

        self.widgets[0].focus_set()

    def on_change(self, field, widget):
        setattr(self.obj, field.column_name, widget.text)

    def is_valid(self):
        for widget in self.widgets:
            if not widget.is_valid():
                return False
        return True

    def save(self):
        if self.is_valid():
            self.session.commit()
            self.destroy()


class CustomerModelForm(Form):
    fields = [
        Field('name', 'Nazwisko', inputs.TextInput, min_length=4, max_length=100),
        Field('street_address', 'Adres', inputs.TextInput, max_length=100),
        Field('postal_code', 'Kod pocztowy', inputs.TextInput, max_length=10),
        Field('city', 'Miasto', inputs.TextInput, max_length=50),
        Field('country', 'Państwo', inputs.TextInput, max_length=50),
    ]
