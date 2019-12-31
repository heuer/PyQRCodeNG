# -*- coding: utf-8 -*-
"""\
Tests against pull request #13
<https://github.com/pyqrcode/pyqrcodeNG/pull/13/>
"""
from __future__ import unicode_literals, absolute_import
import pyqrcodeng


def test_autodetect_binary():
    data = 'Émetteur'
    qr = pyqrcodeng.create(data)
    assert data.encode('iso-8859-1') == qr.data
    assert 'binary' == qr.mode
    assert 'iso-8859-1' == qr.encoding


def test_binary_provide_encoding():
    data = 'Émetteur'
    encoding = 'iso-8859-15'
    qr = pyqrcodeng.create(data, encoding=encoding)
    assert data.encode(encoding) == qr.data
    assert 'binary' == qr.mode
    assert encoding == qr.encoding


def test_forced_binary():
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00:~\x9bU\x00\x00\x00\nIDAT\x08[c\xf8\x0f\x00\x01\x01\x01\x00\x9b\xd7\x1d\r\x00\x00\x00\x00IEND\xaeB`\x82'
    qr = pyqrcodeng.create(data, mode='binary')
    assert 'binary' == qr.mode
    assert qr.encoding is None
    assert data == qr.data


def test_binary():
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x00\x00\x00\x00:~\x9bU\x00\x00\x00\nIDAT\x08[c\xf8\x0f\x00\x01\x01\x01\x00\x9b\xd7\x1d\r\x00\x00\x00\x00IEND\xaeB`\x82'
    qr = pyqrcodeng.create(data)
    assert 'binary' == qr.mode
    assert qr.encoding is None
    assert data == qr.data


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
