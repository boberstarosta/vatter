import tkinter as tk
from .. import db, models, settings, __version__
from .inputs import TextInput, FloatInput, IntInput, ModelChoiceInput
from . import forms, views


class MainWindow(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.option_add('*Font', 'TkFixedFont 14')

        self.title('Vatter {}'.format(__version__))

        frame = tk.Frame(self)
        frame.pack(padx=8, pady=8, fill='both', expand=True)

        tk.Label(frame, text='TextInput:').pack(settings.PACK_STYLE)
        ti = TextInput(frame, min_length=3, max_length=10)
        ti.pack(settings.PACK_STYLE)
        tv = tk.StringVar()
        ti.var.trace('w', lambda *args, i=ti: tv.set(i.text))
        tk.Label(frame, textvariable=tv).pack(settings.PACK_STYLE)

        tk.Label(frame, text='FloatInput:').pack(settings.PACK_STYLE)
        fi = FloatInput(frame, min_value=-10, max_value=1000000)
        fi.pack(settings.PACK_STYLE)
        fv = tk.StringVar()
        fi.var.trace('w', lambda *args, i=fi: fv.set(str(i.value)))
        tk.Label(frame, textvariable=fv).pack(settings.PACK_STYLE)

        tk.Label(frame, text='IntInput:').pack(settings.PACK_STYLE)
        ii = IntInput(frame, min_value=-10, max_value=1000)
        ii.pack(settings.PACK_STYLE)
        iv = tk.StringVar()
        ii.var.trace('w', lambda *args, i=ii: iv.set(str(i.value)))
        tk.Label(frame, textvariable=iv).pack(**settings.PACK_STYLE)

        tk.Label(frame, text='ModelChoiceInput:').pack(**settings.PACK_STYLE)
        mci = ModelChoiceInput(frame, models.Customer, ('name', 'city', 'tax_id_number'))
        mci.pack(**settings.PACK_STYLE)

        tk.Button(frame, text='Open form', command=self.show_customer_form, **settings.BUTTON_STYLE)\
            .pack(**settings.PACK_STYLE)

        tk.Button(frame, text='New inv', command=self.show_invoice_form, **settings.BUTTON_STYLE)\
            .pack(**settings.PACK_STYLE)

        self.setup_geometry()

    def setup_geometry(self):
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        size = tuple(int(a) for a in self.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def show_customer_form(self, customer_id=None):
        if customer_id is None:
            customer = models.Customer()
        else:
            session = db.Session()
            customer = session.query(models.Customer).get(customer_id)
        forms.CustomerForm(self, customer)

    def show_invoice_form(self, invoice_id=None):
        if invoice_id is None:
            invoice = models.Invoice()
        else:
            session = db.Session()
            invoice = session.query(models.Invoice).get(invoice_id)
        forms.InvoiceForm(self, invoice)

    def open_customer_detail(self, customer_id):
        session = db.Session()
        customer = session.query(models.Customer).get(customer_id)
        views.CustomerDetailView(self, customer)
