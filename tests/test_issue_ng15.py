# -*- coding: utf-8 -*-
"""\
Tests against <https://github.com/pyqrcode/pyqrcodeNG/issues/15>
"""
from __future__ import unicode_literals
import pyqrcodeng as pyqrcode
import pytest


def test_version_too_small():
    with pytest.raises(ValueError):
        # QR Code version 1-L: Max. 25 alphanumeric chars
        pyqrcode.create('A' * 26, version=1)


def test_version_and_error_provided():
    # QR Code version 1-L: Max. 25 alphanumeric chars
    qr = pyqrcode.create('A' * 25, version=1)
    assert 1 == qr.version
    assert 'L' == qr.error


if __name__ == '__main__':
    pytest.main([__file__])
