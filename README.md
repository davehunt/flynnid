FlynnID
=======

FlynnID registers a Selenium node to a running Selenium Grid hub.

Installation
------------

From PyPI:

    $ pip install flynnid

From source:

    $ python setup.py install

Running FlynnID
---------------

For full usage details run the following command:

    $ flynnid --help

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -v, --verbose       increase verbosity
    --hubhost=STR       host selenium grid is listening on [default: localhost]
    --hubport=NUM       port selenium grid is listening on [default: 4444]
    --nodehost=STR      host selenium node is listening on [default: localhost]
    --nodeport=NUM      port selenium node is listening on [default: 5555]
    --browsername=STR   name of browser available on node
    --browserver=STR    version of browser available on node
    --platform=STR      platform of node

### Example

Register an AndroidDriver node:

    $ flynnid --nodeport=8080 --browsername=android --browserver=2.3.3 --platform=ANDROID
