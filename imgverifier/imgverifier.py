# -*- coding: utf8 -*-

import os
from PIL import Image

try:
    from os import scandir
except ImportError:
    from scandir import scandir


class ImageVerifier(object):
    """A class for checking and verifying images."""


    @classmethod
    def verify_gen(self, imgdir, exts):
        """Check that all files in a directory are valid images.
        
        Parameters
        ----------
        exts : list of str
            The extensions representing the file types to validate.
        
        Yields
        ------
        tuple (str, list of str)
            The base directory and any paths within that directory that couldn't
            be verified as images.
        """
        filenames = [fn for fn in scandir(imgdir)
                     if os.path.splitext(fn.path)[1].upper() in exts]
        
        corrupt_images = []
        for fn in filenames:
            try:
                img = Image.open(fn.path)
                img.verify()
            except Exception as e:
                corrupt_images.append(fn.path)
                
        yield (os.path.basename(imgdir), corrupt_images)
        
        dirs = [d for d in scandir(imgdir) if d.is_dir()]
        for d in dirs:
            gen = (t for t in ImageVerifier.verify_gen(d.path, exts))
            for p in gen:
                yield p
        