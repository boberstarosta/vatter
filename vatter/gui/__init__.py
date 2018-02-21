import tkinter as tk
from .. import models, settings, __version__
from .inputs import TextInput, FloatInput, IntInput
from . import forms


class MainWindow(tk.Tk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.option_add('*Font', 'times 14')

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

        tk.Button(frame, text='Open form', command=self.show_form, **settings.BUTTON_STYLE).pack(**settings.PACK_STYLE)

        self.setup_geometry()

    def setup_geometry(self):
        self.update()
        self.minsize(self.winfo_width(), self.winfo_height())
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        size = tuple(int(a) for a in self.geometry().split('+')[0].split('x'))
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def show_form(self):
        forms.CustomerForm(self, models.Customer())
