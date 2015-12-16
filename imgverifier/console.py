# -*- coding: utf8 -*-

import Queue
from idlelib.WidgetRedirector import WidgetRedirector

try:
    import tkinter as tk
    from tkinter.ScrolledText import ScrolledText
except ImportError:   # pragma: no cover
    import Tkinter as tk
    from ScrolledText import ScrolledText


class ThreadSafeConsole(ScrolledText):
    """A thread-safe, read-only, scrolling text widget."""


    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.tag_config("ok", foreground="forest green")
        self.tag_config("error", foreground="red")
        self.redir = WidgetRedirector(self)
        self.insert = self.redir.register("insert", lambda *args, **kw: "break")
        self.delete = self.redir.register("delete", lambda *args, **kw: "break")
        self.queue = Queue.Queue()
        self.update()


    def write(self, line):   # pragma: no cover
        self.queue.put(line)


    def clear(self):   # pragma: no cover
        self.queue.put(None)


    def update(self):   # pragma: no cover
        try:
            while True:
                line = self.queue.get_nowait()
                if line is None:
                    self.delete(1.0, tk.END)
                else:

                    parts = line.split('...')
                    self.insert(tk.END, str(parts[0]))
                    if len(parts) > 1:
                        self.insert(tk.END, '...')
                        if str(parts[1]) == 'OK':
                            self.insert(tk.END, str(parts[1]), ('ok'))
                        elif str(parts[1]) == 'ERROR':
                            self.insert(tk.END, str(parts[1]), ('error'))
                        self.insert(tk.END, '\n')

                self.see(tk.END)
                self.update_idletasks()
        except Queue.Empty:
            pass
        self.after(100, self.update)