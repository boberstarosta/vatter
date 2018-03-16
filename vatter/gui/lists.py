import tkinter as tk
from sqlalchemy import or_
from . import db, models, settings


class ModelSelectList(tk.Toplevel):
    model = None
    filter_fields = []

    def __init__(self, parent):
        super().__init__(parent)

        self.session = db.Session()
        self.objects = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.filter_var = tk.StringVar()
        entry = tk.Entry(self, textvariable=self.filter_var,**settings.INPUT_STYLE)
        entry.grid(column=0, row=0, columnspan=2, sticky=tk.EW, **settings.GRID_STYLE)

        frame = tk.Frame(self)
        frame.grid(column=0, row=1, sticky=tk.NSEW, **settings.GRID_STYLE)
        self.listbox = tk.Listbox(frame, **settings.INPUT_STYLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(fill=tk.Y, expand=True)

        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        self.update_listbox()

        self.filter_var.trace('w', self.on_filter_changed)

    def get_queryset(self):
        text = '%' + self.filter_var.get().strip() + '%'
        filter_clauses = [getattr(self.model, field).ilike(text) for field in self.filter_fields]
        return self.session.query(self.model).filter(or_(*filter_clauses)).all()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        self.objects = []
        queryset = self.get_queryset()
        for item in queryset:
            self.listbox.insert(tk.END, str(item))
            self.objects.append(item)

    def on_filter_changed(self, *args):
        self.update_listbox()

    def select(self):
        pass

    def close(self):
        pass


class CustomerSelectList(ModelSelectList):
    model = models.Customer
    filter_fields = ['name', 'tax_id_number']
