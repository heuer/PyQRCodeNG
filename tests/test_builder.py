# -*- coding: utf-8 -*-
"""\
Test against the buidler module.
"""
from __future__ import unicode_literals
import pytest
import pyqrcodeng as pyqrcode
from pyqrcodeng import builder


def test_illegal_mode():
    with pytest.raises(pyqrcode.ModeError):
        builder.QRCodeBuilder('test', 1, mode='murks', error='M')


def test_illegal_error():
    with pytest.raises(pyqrcode.ErrorLevelError):
        builder.QRCodeBuilder('123', version=40, mode='numeric', error='R')


def test_illegal_version():
    with pytest.raises(pyqrcode.VersionError):
        builder.QRCodeBuilder('123', version=41, mode='numeric', error='M')


if __name__ == '__main__':
    pytest.main([__file__])
