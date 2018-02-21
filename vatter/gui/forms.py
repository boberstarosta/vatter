import tkinter as tk
from . import inputs, settings


class Field:
    def __init__(self, caption=None, widget_class=None, **widget_args):
        self.caption = caption
        self.widget_class = widget_class
        self.widget_args = widget_args


class ModelForm(tk.Toplevel):
    fields = []

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

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

        frame = tk.Frame(self)
        frame.pack(side='bottom', fill='x', expand=True)
        tk.Button(frame, text='Zapisz').pack(**settings.PACK_STYLE)


class CustomerModelForm(ModelForm):
    fields = [
        Field('Nazwisko', inputs.TextInput, max_length=100),
        Field('Firma', inputs.TextInput, max_length=100),
        Field('Adres', inputs.TextInput, max_length=100),
        Field('Kod pocztowy', inputs.TextInput, max_length=10),
        Field('Miasto', inputs.TextInput, max_length=50),
        Field('Państwo', inputs.TextInput, max_length=50),
    ]
