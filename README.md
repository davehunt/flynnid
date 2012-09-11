FlynnID
=======

FlynnID registers Selenium nodes to a running Selenium Grid hub.

Installation
------------

From PyPI:

    $ pip install flynnid

From source:

    $ python setup.py install

Running FlynnID
---------------

FlynnID requires either a configuration file in JSON format or command line arguments. Using a configuration
file allows for registration of one or more multiple nodes, whereas the command line arguments only allow for
registration of a single node.

For full usage details run the following command:

    $ flynnid --help

    Usage: flynnid config [options]

    Options:
      --version          show program's version number and exit
      -h, --help         show this help message and exit
      -v, --verbose      increase verbosity
      --force            force registration of node(s)
      --hubhost=str      host selenium grid is listening on [default: localhost]
      --hubport=num      port selenium grid is listening on [default: 4444]
      --nodeconfig=path  configuration file for nodes to register.
      --nodehost=str     host selenium node is listening on [default: localhost]
      --nodeport=num     port selenium node is listening on [default: 5555]
      --browsername=str  name of browser available on node
      --browserver=str   version of browser available on node
      --platform=str     platform of node

### Example: Registering a single node from the command line

    flynnid --nodeport=8080 --browsername=android --browserver=2.3.3 --platform=ANDROID

### Example: Registering multiple nodes from a configuration file

The following would register two AndroidDriver nodes on a local Selenium Grid hub:

    flynnid config.json

Where config.json contains:

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
