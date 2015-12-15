# -*- coding: utf8 -*-

from idlelib.WidgetRedirector import WidgetRedirector

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class ReadOnlyText(tk.Text):
    """Read-only text widget."""

    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.redirector = WidgetRedirector(self)
        self.insert = self.redirector.register("insert", lambda *args,
                                               **kw: "break")
        self.delete = self.redirector.register("delete", lambda *args,
                                                **kw: "break")