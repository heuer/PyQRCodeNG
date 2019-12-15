# -*- coding: utf-8 -*-
"""\
Different tests against the PyQRCode package.
"""
from __future__ import unicode_literals
import pyqrcodeng as pyqrcode
import pytest


_DATA_AUTODETECT = (
    # Input, expected version, expected mode
    ('123456', 'numeric'),
    (123456, 'numeric'),
    ('123A', 'alphanumeric'),
    ('123a', 'binary'),
    ('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:', 'alphanumeric'),
    ('HELLO WORLD', 'alphanumeric'),
    ('HELLO\nWORLD', 'binary'),
    ('MÄRCHENBUCH', 'binary'),
    ('®', 'binary'),
    ('http://www.example.org/', 'binary'),
    ('http://www.example.org/path/index.html', 'binary'),
    ('点', 'kanji'),
    ('茗', 'kanji'),
    ('漢字', 'kanji'),
    ('外来語', 'kanji'),
)


@pytest.mark.parametrize('data, expected_mode', _DATA_AUTODETECT)
def test_valid_mode_autodetection(data, expected_mode):
    qr = pyqrcode.create(data)
    assert expected_mode == qr.mode


@pytest.mark.parametrize('data, expected_mode', _DATA_AUTODETECT)
def test_valid_mode_provided(data, expected_mode):
    qr = pyqrcode.create(data, mode=expected_mode)
    assert expected_mode == qr.mode


_DATA_INVALID_MODE = (
    # Input, invalid mode
    ('a', 'alphanumeric'),
    ('b', 'numeric'),
    ('C', 'numeric'),
    ('HELLO\nWORLD', 'alphanumeric'),
    ('MÄRCHENBUCH', 'alphanumeric'),
    ('http://www.example.org/', 'alphanumeric'),
    ('http://www.example.org/', 'unknown'),
)


@pytest.mark.parametrize('data, mode', _DATA_INVALID_MODE)
def test_invalid_mode_provided(data, mode):
    with pytest.raises(ValueError):
        pyqrcode.create(data, mode=mode)


def test_binary_data():
    qr = pyqrcode.create('Märchenbuch'.encode('utf-8'), encoding='utf-8')
    assert 'Märchenbuch' == qr.data
    assert 'binary' == qr.mode


def test_unicode_utf8():
    s = '\u263A'  # ☺ (WHITE SMILING FACE)
    try:
        pyqrcode.create(s, encoding='latin1')
        raise Exception('Expected an error for \u263A and ISO-8859-1')
    except ValueError:
        pass
    qr = pyqrcode.create(s, encoding='utf-8')
    assert 'binary' == qr.mode


def test_kanji_detection():
    s = '点茗' #Characters directly from the standard
    qr = pyqrcode.create(s)
    assert 'kanji' == qr.mode
    assert s.encode('shiftjis') == qr.builder.data


def test_kanji_encoding():
    s = '点茗' #Characters directly from the standard

    #These come from a reference image passed through the debugger
    codewords = [128,38,207,234,168,0,236,17,236,18,75,55,241,75,140,21,
                 117,174,242,221,243,87,199,123,50,169]
    
    qr = pyqrcode.create(s)

    #Get the binary representation of the data for the code
    bin_words = qr.builder.buffer.getvalue()

    #Convert the data into integer bytes
    b = [int(bin_words[i:i+8], base=2) for i in range(0, len(bin_words), 8)]
    #See if the calculated code matches the known code
    assert b == codewords


def test_kanji_tranform_encoding():
    """Test the encoding can be set to shiftjis for utf-8 encoding.
    """
    s = 'モンティ'
    s = '点茗' #Characters directly from the standard
    
    #Encode the string as utf-8 *not* shiftjis
    utf8 = s.encode('utf-8')
    qr = pyqrcode.create(utf8, encoding='utf-8')
    assert qr.mode == 'kanji'
    assert qr.encoding == 'shiftjis'
    

def test_kanji_enforce_binary():
    data = '点'
    # 1. Try usual mode --> kanji
    qr = pyqrcode.create(data)
    assert 'kanji' == qr.mode
    # 2. Try another encoding --> binary
    qr = pyqrcode.create(data, mode='binary', encoding='utf-8')
    assert 'binary' == qr.mode


def test_kanji_enforce_binary2():
    data = '点'
    qr = pyqrcode.create(data.encode('utf-8'))
    assert 'binary' == qr.mode


def test_kanji_bytes():
    data = '外来語'
    qr = pyqrcode.create(data.encode('shift_jis'))
    assert 'kanji' == qr.mode


def test_to_str():
    s = 'Märchen'
    assert str(pyqrcode.create(s))

    s = '外来語'
    qr = pyqrcode.create(s)
    assert str(pyqrcode.create(s))


def test_invalid_version():
    with pytest.raises(ValueError):
        pyqrcode.create('test', version=41)


def test_invalid_version2():
    with pytest.raises(ValueError):
        pyqrcode.create('test', version=0)


def test_invalid_mode():
    with pytest.raises(ValueError):
        pyqrcode.create('test', mode='alpha')


def test_invalid_mode2():
    with pytest.raises(ValueError):
        pyqrcode.create('test', mode='')


def test_kanji_not_supported():
    with pytest.raises(ValueError):
        pyqrcode.create('test', mode='kanji')


def test_invalid_ecc():
    with pytest.raises(ValueError):
        pyqrcode.create('test', error='R')


def test_forced_binary():
    data = 'Émetteur'.encode('iso-8859-15')
    qr = pyqrcode.create(data, mode='binary')
    assert qr.data == data
    assert qr.mode == 'binary'


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])

