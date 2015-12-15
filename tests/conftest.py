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
def app():
    return View()


@pytest.fixture
def imgdir(tmpdir):
    imgdir = tmpdir.mkdir('images')
    for i in range(5):
        fn = 'img_{}.jpg'.format(i)
        imgdir.join(fn).write('content')
    return str(tmpdir)
