# -*- coding: utf8 -*-

import os
import pytest
import tempfile
from io import BytesIO
from PIL import Image
from imgverifier.view import View

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


@pytest.fixture(scope='session')
def tk_app():
    return View()


@pytest.fixture
def imgdir(tmpdir):
    imgdir = tmpdir.mkdir('images')
    for i in range(5):
        fn = 'img_{}.txt'.format(i)
        imgdir.join(fn).write("content")
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    fn = imgdir.join('img.jpg')
    image.save(str(fn))
    return str(imgdir)



def create_image(tmpdir_factory):
    image = Image.new('RGBA', size=(50, 50), color=(155, 0, 0))
    fn = tmpdir_factory.mktemp('images').join('img.png')
    image.save(str(fn))
    return tmp