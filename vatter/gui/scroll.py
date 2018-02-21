import platform
from tkinter import *

OS = platform.system()


class VScrollFrame(Frame):
    """
        Usage:
            Use the 'interior' attribute to place widgets inside the
            scrollable frame construct and pack/place/grid normally.
    """

    active_widget = None

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        self.canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)

        vscrollbar.config(command=self.canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = interior = Frame(self.canvas)
        interior_id = self.canvas.create_window(0, 0, window=interior, anchor=NW)

        def _configure_interior(event):
            self.canvas.config(scrollregion=self.canvas.bbox(ALL))
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

        self.interior.bind("<Enter>", lambda e: self._set_active())
        self.interior.bind("<Leave>", lambda e: self._set_inactive())

        on_mousewheel = self._get_mousewheel_handler()

        if OS == "Linux":
            self.bind_all('<4>', on_mousewheel)
            self.bind_all('<5>', on_mousewheel)
        else:
            self.bind_all("<MouseWheel>", on_mousewheel)

    @staticmethod
    def _get_mousewheel_handler():
        if OS == "Linux":
            def on_mousewheel(event):
                if VScrollFrame.active_widget is not None:
                    if event.num == 4:
                        VScrollFrame.active_widget.canvas.yview_scroll(-1, "units")
                    elif event.num == 5:
                        VScrollFrame.active_widget.canvas.yview_scroll(1, "units")
        elif OS == "Windows":
            def on_mousewheel(event):
                if VScrollFrame.active_widget is not None:
                    VScrollFrame.active_widget.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        else:
            def on_mousewheel(event):
                pass

        return on_mousewheel

    def _set_active(self):
        VScrollFrame.active_widget = self

    @classmethod
    def _set_inactive(cls):
        cls.active_widget = None
