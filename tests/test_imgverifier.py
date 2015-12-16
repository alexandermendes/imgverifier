# -*- coding: utf8 -*-

import pytest
from imgverifier.verifier import ImageVerifier
from imgverifier.view import View

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk


class TestImageVerifier():
        
    
    def test_bad_images_identified(self, imgdir):
        data = [d for d in ImageVerifier.verify_gen(imgdir, ['.JPG'])]

        assert len(data[1][1]) == 5
        
    
    def test_report_ok(self, app):
        app.text.delete(1.0, tk.END)
        app.report('dir', [])
        text = app.text.get('1.0', 'end-1c')
        print(text)
        
        assert text.startswith('dir...OK')
    
    
    def test_report_error(self, app):
        app.text.delete(1.0, tk.END)
        app.report('dir', ['bad_image'])
        text = app.text.get('1.0', 'end-1c')
        
        assert text.startswith('dir...ERROR')
    
    
    def test_final_report(self, app):
        app.text.delete(1.0, tk.END)
        app.final_report()
        text = app.text.get('1.0', 'end-1c')
        
        assert text.endswith('\nDONE...all files were verified')