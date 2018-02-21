import tkinter as tk


class CustomerDetailView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        data_frame = tk.Frame(self)
        data_frame.pack(fill='both', expand=True)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(fill='x', expand=True)
        tk.Button(buttons_frame, text='Edytuj').pack(side='left', **settings.PACK_STYLE)
        tk.Button(buttons_frame, text='Usuń').pack(side='left', **settings.PACK_STYLE)
        tk.Button(buttons_frame, text='Zamknij').pack(side='left', **settings.PACK_STYLE)
