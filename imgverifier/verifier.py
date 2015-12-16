# -*- coding: utf8 -*-

import os
from PIL import Image

try:
    from os import scandir
except ImportError:   # pragma: no cover
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
            The path of the directory and any filenames within that directory
            that couldn't be verified as images.
        """
        non_images = []
        filenames = []
        dirs = []
        for f in scandir(imgdir):
            if f.is_dir():
                dirs.append(f)
            elif os.path.splitext(f.path)[1].upper() in exts:
                filenames.append(f)

        for fn in filenames:
            try:
                img = Image.open(fn.path)
                img.verify()
            except Exception:
                non_images.append(fn.name)

        yield (imgdir, non_images)

        for d in dirs:
            gen = (t for t in ImageVerifier.verify_gen(d.path, exts))
            for p in gen:
                yield p
