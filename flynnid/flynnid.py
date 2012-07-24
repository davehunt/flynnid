#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from optparse import OptionParser
import json
import os
import sys
import urllib2

def main ():
    usage = "Usage: %prog [options] config"
    parser = OptionParser(usage=usage, version='%prog 0.2')
    parser.set_defaults(verbose=False)
    parser.add_option('-v', '--verbose',
                      action='store_true',
                      help='increase verbosity')
    (options, args) = parser.parse_args()

    if len(args) < 1:
        sys.exit('ERROR: Configuration file not specified!')

    if not os.path.exists(args[0]):
        sys.exit('ERROR: Configuration file %s not found!' % args[0])

    config = json.load(open(args[0]))

    hub_host = config['hub']['host']
    hub_port = config['hub']['port']

    url = 'http://%s:%i/grid/register' % (hub_host, hub_port)

    for node in config['nodes']:
        node_host = node['host']
        node_port = node['port']
        data = {
            'class': 'org.openqa.grid.common.RegistrationRequest',
            'capabilities': [{
                'seleniumProtocol': 'WebDriver',
                'browserName': node['browser']['name'],
                'version': node['browser']['version'],
                'platform': node['platform'],
                'maxInstances': 1}],
            'configuration': {
                'port': node_port,
                'host': node_host,
                'proxy': 'org.openqa.grid.selenium.proxy.DefaultRemoteProxy',
                'register': True,
                'registerCycle': 5000,
                'hubHost': config['hub']['host'],
                'hub': 'http://%s:%i/grid/register' % (hub_host, hub_port),
                'url': 'http://%s:%i' % (node_host, node_port),
                'remoteHost': 'http://%s:%i' % (node_host, node_port),
                'maxSession': 1,
                'role': 'node',
                'hubPort': hub_port}}
        data = json.dumps(data)
        if options.verbose:
            print 'Using JSON request: %s' % data

        print 'Registering node to hub: %s' % url
        request = urllib2.Request(url, data)
        try:
            urllib2.urlopen(request)
            print 'Success!'
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'Unable to connect to Selenium Grid hub! Is it running?'
                print 'Reason: %s' % e.reason
            elif hasattr(e, 'code'):
                print 'Registration to Selenium Grid hub failed!'
                print 'URL: %s' % e.geturl()
                print 'Error code: %s' % e.code


if __name__ == '__main__':
    main()
