__version__ = '0.0.dev0'


def start():
    from . import db, models
    models.Base.metadata.create_all(db.engine)

    from .gui import MainWindow
    main_window = MainWindow()
    main_window.mainloop()
