# -*- coding: utf8 -*-

from idlelib.WidgetRedirector import WidgetRedirector

try:
    import tkinter as tk
    from tkinter.scrolledtext import ScrolledText
    import queue
except ImportError:   # pragma: no cover
    import Tkinter as tk
    from ScrolledText import ScrolledText
    import Queue as queue


class ThreadSafeConsole(ScrolledText):
    """A thread-safe, read-only, scrolling text widget."""


    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)
        self.tag_config("ok", foreground="forest green")
        self.tag_config("error", foreground="red")
        self.redir = WidgetRedirector(self)
        self.insert = self.redir.register("insert", lambda *args, **kw: "break")
        self.delete = self.redir.register("delete", lambda *args, **kw: "break")
        self.queue = queue.Queue()
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
                        suffix = str(parts[1]) 
                        self.insert(tk.END, '...')
                        if suffix.endswith('OK'):
                            suffix = suffix.replace('OK', '')
                            self.insert(tk.END, suffix)
                            self.insert(tk.END, 'OK', ('ok'))
                        elif suffix.startswith('ERROR'):
                            suffix = suffix.replace('ERROR', '')
                            self.insert(tk.END, 'ERROR', ('error'))
                            self.insert(tk.END, suffix)
                        else:
                            self.insert(tk.END, suffix)
                        self.insert(tk.END, '\n')

                self.see(tk.END)
                self.update_idletasks()
        except queue.Empty:
            pass
        self.after(100, self.update)