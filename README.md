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

FlynnID requires a configuration file in JSON format to be specified on the command line.

For full usage details run the following command:

    $ flynnid --help

    --version           show program's version number and exit
    -h, --help          show this help message and exit
    -v, --verbose       increase verbosity

### Example configuration

The following would register two AndroidDriver nodes on a local Selenium Grid hub:

    {
        "hub": {
            "host": "localhost",
            "port": 4444
        },
        "nodes": [{
            "host": "10.250.10.10",
            "port": 8080,
            "browser": {
                "name": "android",
                "version": "4"
            },
            "platform": "ANDROID"
        },{
            "host": "10.250.10.11",
            "port": 8080,
            "browser": {
                "name": "android",
                "version": "4"
            },
            "platform": "ANDROID"
        }]
    }
