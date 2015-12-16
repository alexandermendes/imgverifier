# -*- coding: utf8 -*-

import os
import pytest
import time
from imgverifier.verifier import ImageVerifier
from imgverifier.view import View
from imgverifier.console import ThreadSafeConsole
import Queue

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class TestImageVerifier():
        
    
    def test_invalid_extensions_ignored(self, imgdir):
        data = [d for d in ImageVerifier.verify_gen(imgdir, ['.PNG'])]

        assert len(data[0][1]) == 0
    
    
    def test_bad_images_identified(self, imgdir):
        data = [d for d in ImageVerifier.verify_gen(imgdir, ['.TXT', '.JPG'])]

        assert len(data[0][1]) == 5
    
    
    def test_good_images_identified(self, imgdir):
        data = [d for d in ImageVerifier.verify_gen(imgdir, ['.JPG'])]

        assert len(data[0][1]) == 0
    
    
    def test_sub_dirs_checked(self, imgdir):
        base = os.path.dirname(str(imgdir))
        data = [d for d in ImageVerifier.verify_gen(base, ['.JPG'])]

        assert len(data) > 1
    
    
    def test_bad_images_identified_in_sub_dirs(self, imgdir):
        base = os.path.dirname(str(imgdir))
        data = [d for d in ImageVerifier.verify_gen(base, ['.TXT'])
                if d[0] == 'images']

        assert len(data[0][1]) == 5


    def test_report_ok(self, tk_app):
        tk_app.console.delete(1.0, tk.END)
        text = tk_app.get_report('dir', [])
        
        assert text.startswith('dir...OK')


    def test_report_error(self, tk_app):
        tk_app.console.delete(1.0, tk.END)
        text = tk_app.get_report('dir', ['bad_image'])
        
        assert text.startswith('dir...ERROR')


    def test_get_final_report_all_verified(self, tk_app):
        tk_app.console.delete(1.0, tk.END)
        tk_app.corrupt_images = []
        text = tk_app.get_final_report()
        
        assert text.endswith('\nDONE...all files were verified.')
    
    
    def test_get_final_report_one_error(self, tk_app):
        tk_app.console.delete(1.0, tk.END)
        tk_app.corrupt_images = ['error']
        text = tk_app.get_final_report()
        
        assert text.endswith("\nDONE...1 file couldn't be verified.")
    
    
    def test_get_final_report_multiple_errors(self, tk_app):
        tk_app.console.delete(1.0, tk.END)
        tk_app.corrupt_images = ['error', 'error']
        text = tk_app.get_final_report()
        
        assert text.endswith("\nDONE...2 files couldn't be verified.")
    
    
    def test_write_to_console(self):
        console = ThreadSafeConsole()
        
        console.write('hello')

        assert console.get('1.0', 'end-1c') == "hello"
