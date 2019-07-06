QR Code creation from the command line
======================================

The command line script "pyqr" can be used to print QR Codes to the command
line or to serialize QR Codes.


Usage
-----

Output the QR Code to the terminal::

    $ pyqr "Little wing"


Version
^^^^^^^

If the ``version`` parameter is not provided, pyqr chooses the minimal version
for the QR Code automatically. The version may be specified as an integer.

The content 'Layla' would fit into a version 1 QR Code, but the following commands
enforce version 5::

    $ pyqr --version=5 Layla
    $ pyqr -v=5 Layla


Error correction level
^^^^^^^^^^^^^^^^^^^^^^

The default error correction level is "H", use the ``error`` parameter to change
it::

    $ pyqr --error=q "Ain't no grave"
    $ pyqr -e=m "Heart of Gold"


QR Code serialization
^^^^^^^^^^^^^^^^^^^^^

Printing the QR Codes to the terminal is nice but the ``output`` parameter
serializes the QR Code in one of the supported file formats::

    $ pyqr --output=white-room.png "White Room"
    $ pyqr -o=satellite.svg "Satellite Of Love"
    $ pyqr --output=mrs.eps "Mrs. Robinson"


Scaling QR Codes
^^^^^^^^^^^^^^^^

If the resulting QR Code is too small, ``scale`` can be used to create a more
appropriate output::

    $ pyqr --scale=10 --output=money-talks.png "Money Talks"
    $ pyqr -s 10 --output=private-investigations.svg Private Investigations


If the serializer does not support a scaling factor (i.e. text output), this
parameter is ignored.


Changing the size of the quiet zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The generated QR Codes will have a recommended quiet zone around the
symbol. To change the size of the quiet zone, ``quietzone`` can be utilized::

    $ pyqr --quietzone=0 --output=black-magic-woman.svg "Black Magic Woman"
    $ pyqr --qz=10 --output=diamond.png "Shine On You Crazy Diamond"
