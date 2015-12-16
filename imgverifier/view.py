# -*- coding: utf8 -*-

import threading
from imgverifier.verifier import ImageVerifier
from imgverifier.console import ThreadSafeConsole
 
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
 
        self.console = ThreadSafeConsole(f1, width=120)
       
        self.ext = tk.Entry(f2, textvariable=self.ext_var)
        ext_lbl = tk.Label(f2, text='Extensions:')
        check_btn = tk.Button(f2, text="Run",
                              command=self.on_check_dir, width=15)
        save_btn = tk.Button(f2, text="Save",
                             command=self.on_save, width=15)
 
        grid_opts = {'padx': 20, 'pady': 5, 'sticky': 'e'}
        f1.pack(anchor=tk.N, fill=tk.BOTH, expand=True, side=tk.TOP)
        f2.pack(anchor=tk.E, side=tk.BOTTOM)
        f2.columnconfigure(1, weight=1)
        self.console.grid(column=0, row=0, **grid_opts)
        ext_lbl.grid(column=0, row=1, **grid_opts)
        self.ext.grid(column=1, row=1)
        save_btn.grid(column=2, row=1, **grid_opts)
        check_btn.grid(column=3, row=1, **grid_opts)
       
 
    def on_check_dir(self):   # pragma: no cover
        """Ask for an image directory and check it for corrupt images."""
        exts = ['.{}'.format(e.strip().upper())
                for e in self.ext_var.get().split(',') if len(e.strip()) > 0]
       
        basedir = tkFileDialog.askdirectory()
        if basedir:
            self.console.clear()
                
            def worker():
                verified = ImageVerifier.verify_gen(basedir, exts)
                
                for imgdir, path in verified:
                    self.corrupt_images += path
                    msg = self.get_report(imgdir, path)
                    self.console.write(msg)

                msg = self.get_final_report()
                self.console.write(msg)

        t = threading.Thread(target=worker)
        t.start()


    def get_report(self, imgdir, paths):
        """Report the outcome of checking a directory."""
        msg = '{}...'.format(imgdir)
        
        if len(paths) == 0:
            msg += 'OK'
        
        else:
            msg += 'ERROR'

            for p in paths:
                msg += '   -{0}\n'.format(p)
        
        return msg
 
 
    def get_final_report(self):
        """Report the final outcome of checking a directory."""
        msg = '\nDONE...'
        
        n = len(self.corrupt_images)
        if n == 0:
            msg += 'all files were verified.'
        elif n == 1:
            msg += "{} file couldn't be verified.".format(n)
        else:
            msg += "{} files couldn't be verified.".format(n)
        
        return msg

 
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
