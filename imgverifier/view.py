# -*- coding: utf8 -*-

import threading
from imgverifier.verifier import ImageVerifier
from imgverifier.read_only_text import ReadOnlyText
 
try:
    import tkinter as tk
    import tkinter.filedialog as tkFileDialog
except ImportError:   # pragma: no cover
    import Tkinter as tk
    import tkFileDialog
 
 
class View(tk.Tk):
 
    def __init__(self):
        tk.Tk.__init__(self, None)
        self.resizable(0,0)
        self.title("Image Verifier")
        self.corrupt_images = []
 
        self.ext_var = tk.StringVar(self, 'tiff,tif,jpg,jpeg')
 
        f1 = tk.Frame(self)
        f2 = tk.Frame(self)
 
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text = ReadOnlyText(f1, yscrollcommand=scrollbar.set)
        self.text.tag_config("ok", foreground="forest green")
        self.text.tag_config("error", foreground="red")
        scrollbar.config(command=self.text.yview)
       
        self.ext = tk.Entry(f2, textvariable=self.ext_var, width=40)
        ext_lbl = tk.Label(f2, text='Extensions:')
        check_btn = tk.Button(f2, text="Run",
                              command=self.on_check_dir, width=15)
        save_btn = tk.Button(f2, text="Save",
                             command=self.on_save, width=15)
 
        grid_opts = {'padx': 20, 'pady': 5, 'sticky': 'e'}
        f1.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.TOP)
        f1.rowconfigure(0, weight=1)
        f2.pack(anchor=tk.E, fill=tk.BOTH, expand=True, side=tk.BOTTOM)
        f2.columnconfigure(1, weight=1)
        self.text.grid(column=0, row=0, **grid_opts)
        ext_lbl.grid(column=0, row=1, **grid_opts)
        self.ext.grid(column=1, row=1)
        save_btn.grid(column=2, row=1, **grid_opts)
        check_btn.grid(column=3, row=1, **grid_opts)
       
 
    def on_check_dir(self):   # pragma: no cover
        """Ask for an image directory and check it for corrupt images."""
        def worker():
            exts = ['.{}'.format(e.strip().upper())
                    for e in self.ext_var.get().split(',')
                    if len(e.strip()) > 0]
           
            basedir = tkFileDialog.askdirectory()
            if basedir:
                self.text.delete(1.0, tk.END)
                verified = ImageVerifier.verify_gen(basedir, exts)
                
                for imgdir, path in verified:
                    self.report(imgdir, path)
                    self.corrupt_images += path

                self.final_report()

        t = threading.Thread(target=worker)
        t.start()


    def report(self, imgdir, paths):
        """Report the outcome of checking a directory."""        
        self.text.insert(tk.INSERT, '{}...'.format(imgdir))
        
        if len(paths) == 0:
            self.text.insert(tk.INSERT, 'OK\n', ('ok'))
        
        else:
            self.text.insert(tk.INSERT, 'ERROR\n', ('error'))
            for p in paths:
                self.text.insert(tk.INSERT, '   -{0}\n'.format(p))

        self.text.see(tk.END)
 
 
    def final_report(self):
        self.text.insert(tk.END, '\nDONE...')
        
        n = len(self.corrupt_images)
        if n == 0:
            self.text.insert(tk.END, 'all files were verified.')
        elif n == 1:
            self.text.insert(tk.END, "{} file couldn't be verified.".format(n))
        else:
            self.text.insert(tk.END, "{} files couldn't be verified.".format(n))
        
        self.text.see(tk.END)

 
    def on_save(self):   # pragma: no cover 
        """Save the list of non-images to a text file."""
        opts = {'title':  'Save',
                'filetypes': [('Text File', '.txt')],
                'defaultextension': '.txt',
                'initialfile': 'Corrupted.txt'}
 
        savefile = tkFileDialog.asksaveasfilename(**opts)
        if savefile:
            with open(savefile, 'w') as out:
                for path in self.corrupt_images:
                    out.write('{0}\n'.format(path))
