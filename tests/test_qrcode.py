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
    data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00B\x00\x00\x00B\x01\x00\x00\x00\x00\xcb/=E\x00\x00\x00\x9cIDATx\x9c\xad\xd2\xb1\n\x041\x08\x04P\xc1V\xc8\xaf\x08\xb6\x81\xf9ua\xdb\x80\xbfr`\xbb\xe0]\xb1)\xcc\xb5;\xd5\xabF\x8b\xa1z\xe2\xf4\x92\x88\x97*\xa1\t\xc9e\xd5\xa56\xd5\xf8\x94\xf9\xbfF\xe4!\xa4\xc5\xee\xdb"6\xdbw\xb7~Y\xd8\xff=J\xe7\x10\xea\x1aQ\x13\x17\x9an\x85\xcf\xec\x92\xe2a\xab\x9a\xea\x9a\x8aC\x9fr\x9b\xd1%\xca\xc1\xdaU\xb0%\x0bMD#hvU\xc9\x8dQM\xc4$\xc6]H-H\x97\xdag\xd1<u\xf9=NM1B\x13\xf2J\x8fj"v\xc4@\xd3\xbb\x1b\xfa\x02\xcb\xecz\xee\x93\xda\xe9(\x00\x00\x00\x00IEND\xaeB`\x82'
    qr = pyqrcode.create(data, mode='binary')
    assert qr.data == data
    assert qr.mode == 'binary'


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])

