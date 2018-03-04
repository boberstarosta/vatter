import tkinter as tk
from . import inputs, models, settings
from .. import db


class Field:
    def __init__(self, column_name, caption=None, widget_class=None, **widget_args):
        self.column_name = column_name
        self.caption = caption
        self.widget_class = widget_class
        self.widget_args = widget_args


class Form(tk.Toplevel):
    fields = None

    def __init__(self, parent, obj):
        super().__init__(parent)

        self.title('Klient')

        self.session = db.Session()
        self.obj = self.session.merge(obj)

        frame = tk.Frame(self)
        frame.pack(fill='both', expand=True)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.widgets = []

        for i, field in enumerate(self.fields):
            frame.grid_rowconfigure(i, weight=1)
            tk.Label(frame, text=field.caption + ':', anchor='e')\
                .grid(column=0, row=i, sticky='ew', **settings.GRID_STYLE)
            widget = field.widget_class(frame, **field.widget_args)
            widget.grid(column=1, row=i, sticky='ew', **settings.GRID_STYLE)
            self.widgets.append(widget)
            value = getattr(self.obj, field.column_name)
            if value is not None:
                widget.var.set(value)
            widget.var.trace('w', lambda *args, f=field, w=widget: self.on_change(f, w))

        frame = tk.Frame(self)
        frame.pack(side='bottom', fill='x', expand=True)
        tk.Button(frame, text='Zapisz', command=self.save, **settings.BUTTON_STYLE)\
            .pack(side='left', **settings.PACK_STYLE)
        tk.Button(frame, text='Zamknij', command=self.cancel, **settings.BUTTON_STYLE)\
            .pack(side='left', **settings.PACK_STYLE)

        self.bind('<Return>', lambda *args: self.save())
        self.bind('<KP_Enter>', lambda *args: self.save())
        self.bind('<Escape>', lambda *args: self.cancel())

        self.widgets[0].focus_set()

    def on_change(self, field, widget):
        setattr(self.obj, field.column_name, widget.text)

    def is_valid(self):
        for widget in self.widgets:
            if not widget.is_valid():
                widget.focus_set()
                return False
        return True

    def save(self):
        if self.is_valid():
            self.session.commit()
            self.destroy()
            self.master.open_customer_detail(self.obj.id)

    def cancel(self):
        self.destroy()


class CustomerForm(Form):
    fields = [
        Field('name', 'Nazwa', inputs.TextInput, min_length=4, max_length=100),
        Field('street_address', 'Adres', inputs.TextInput, max_length=100),
        Field('postal_code', 'Kod pocztowy', inputs.TextInput, max_length=10),
        Field('city', 'Miasto', inputs.TextInput, max_length=50),
        Field('country', 'Państwo', inputs.TextInput, max_length=50),
        Field('tax_id_number', 'NIP', inputs.TextInput, max_length=20),
    ]


class InvoiceForm(tk.Toplevel):
    def __init__(self, parent, obj):
        super().__init__(parent)

        self.title('Faktura')

        self.session = db.Session()
        self.obj = self.session.merge(obj)

        frame = tk.Frame(self)
        frame.pack(fill='both', expand=True)

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.widgets = []

        buyer_field = Field('buyer_id', 'Kupujący', inputs.ModelChoiceInput, model=models.Customer,
                            filter_fields=('name', 'city', 'tax_id_number'))

        frame.grid_rowconfigure(0, weight=1)
        tk.Label(frame, text=buyer_field.caption + ':', anchor='e')\
            .grid(column=0, row=0, sticky='ew', **settings.GRID_STYLE)
        widget = buyer_field.widget_class(frame, **buyer_field.widget_args)
        widget.grid(column=1, row=0, sticky='ew', **settings.GRID_STYLE)
        value = getattr(self.obj, buyer_field.column_name)
        if value is not None:
            widget.var.set(value)
        widget.var.trace('w', lambda *args, f=buyer_field, w=widget: self.on_change(f, w))
        self.widgets.append(widget)

        frame = tk.Frame(self)
        frame.pack(side='bottom', fill='x', expand=True)
        tk.Button(frame, text='Zapisz', command=self.save, **settings.BUTTON_STYLE)\
            .pack(side='left', **settings.PACK_STYLE)
        tk.Button(frame, text='Zamknij', command=self.cancel, **settings.BUTTON_STYLE)\
            .pack(side='left', **settings.PACK_STYLE)

    def on_change(self, field, widget):
        setattr(self.obj, field.column_name, widget.get_selected_object().id)

    def is_valid(self):
        for widget in self.widgets:
            if not widget.is_valid():
                widget.focus_set()
                return False
        return True

    def save(self):
        if self.is_valid():
            self.session.commit()
            self.destroy()

    def cancel(self):
        self.destroy()
