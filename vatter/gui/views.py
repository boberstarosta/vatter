import tkinter as tk
from .. import db, settings


class Field:
    def __init__(self, column_name, caption):
        self.column_name = column_name
        self.caption = caption


class DetailView(tk.Toplevel):
    fields = None

    def __init__(self, parent, obj):
        super().__init__(parent)
        self.session = db.Session()
        self.obj = obj

        data_frame = tk.Frame(self)
        data_frame.pack(fill='both', expand=True)
        data_frame.grid_columnconfigure(0, weight=1)
        data_frame.grid_columnconfigure(1, weight=1)

        for i, field in enumerate(self.fields):
            data_frame.grid_rowconfigure(i, weight=1)
            tk.Label(data_frame, text=field.caption + ':', anchor='e')\
                .grid(column=0, row=i, sticky='ew', **settings.GRID_STYLE)
            tk.Label(data_frame, text=getattr(self.obj, field.column_name), anchor='w', width=80)\
                .grid(column=1, row=i, sticky='ew', **settings.GRID_STYLE)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill='x', expand=True)
        tk.Button(buttons_frame, text='Edytuj', **settings.BUTTON_STYLE, command=self.edit)\
            .pack(side='left', **settings.PACK_STYLE)
        tk.Button(buttons_frame, text='Usuń', **settings.BUTTON_STYLE, command=self.delete)\
            .pack(side='left', **settings.PACK_STYLE)
        tk.Button(buttons_frame, text='Zamknij', **settings.BUTTON_STYLE, command=self.close)\
            .pack(side='left', **settings.PACK_STYLE)

    def edit(self):
        self.destroy()
        self.master.show_customer_form(self.obj.id)

    def delete(self):
        # TODO: Display confirmation dialog and delete
        pass

    def close(self):
        self.destroy()


class CustomerDetailView(DetailView):
    fields = [
        Field('name', 'Nazwa'),
        Field('street_address', 'Adres'),
        Field('postal_code', 'Kod pocztowy'),
        Field('city', 'Miasto'),
        Field('country', 'Państwo'),
        Field('tax_id_number', 'NIP'),
    ]
