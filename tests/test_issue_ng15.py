# -*- coding: utf-8 -*-
"""\
Tests against <https://github.com/pyqrcode/pyqrcodeNG/issues/15>
"""
from __future__ import unicode_literals
import pyqrcodeng as pyqrcode
import pytest


def test_version_too_small():
    with pytest.raises(pyqrcode.DataOverflowError):
        # QR Code version 1-L: Max. 25 alphanumeric chars
        pyqrcode.create('A' * 26, version=1, error='l')


def test_numeric_defaults():
    qr = pyqrcode.create('1' * 17)  # Capacity of a 1-H (numeric): 17
    assert '1-H' == qr.designator
    assert 'numeric' == qr.mode


def test_numeric_explicit_error():
    qr = pyqrcode.create('1' * 41, error='l')  # Capacity of a 1-L (numeric): 41
    assert '1-L' == qr.designator
    assert 'numeric' == qr.mode


def test_version_and_error_provided():
    # QR Code version 1-L: Max. 25 alphanumeric chars
    qr = pyqrcode.create('A' * 25, version=1, error='l')
    assert 1 == qr.version
    assert 'L' == qr.error
    assert '1-L' == qr.designator
    assert 'alphanumeric' == qr.mode


if __name__ == '__main__':
    pytest.main([__file__])
