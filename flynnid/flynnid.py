#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from optparse import OptionParser
import json
import os
import sys
import urllib2

from termcolor import colored


def main ():
    from colorama import init
    init()

    usage = "Usage: %prog config [options]"
    parser = OptionParser(usage=usage, version='%prog 0.3')
    parser.set_defaults(verbose=False)
    parser.add_option('-v', '--verbose',
                      action='store_true',
                      help='increase verbosity')
    parser.add_option('--force',
                      action='store_true',
                      help='force registration of node(s)')
    parser.add_option('--hubhost',
                      action='store',
                      type='string',
                      metavar='str',
                      dest='hub_host',
                      default='localhost',
                      help='host selenium grid is listening on [default: %default]')
    parser.add_option('--hubport',
                      action='store',
                      type='int',
                      metavar='num',
                      dest='hub_port',
                      default=4444,
                      help='port selenium grid is listening on [default: %default]')
    parser.add_option('--nodeconfig',
                      action='store',
                      type='string',
                      metavar='path',
                      dest='node_config',
                      help='configuration file for nodes to register.')
    parser.add_option('--nodehost',
                      action='store',
                      type='string',
                      metavar='str',
                      dest='node_host',
                      default='localhost',
                      help='host selenium node is listening on [default: %default]')
    parser.add_option('--nodeport',
                      action='store',
                      type='int',
                      metavar='num',
                      dest='node_port',
                      default=5555,
                      help='port selenium node is listening on [default: %default]')
    parser.add_option('--browsername',
                      action='store',
                      type='str',
                      metavar='str',
                      dest='browser_name',
                      help='name of browser available on node')
    parser.add_option('--browserver',
                      action='store',
                      type='str',
                      metavar='str',
                      dest='browser_version',
                      help='version of browser available on node')
    parser.add_option('--platform',
                      action='store',
                      type='str',
                      metavar='str',
                      help='platform of node')
    (options, args) = parser.parse_args()

    if len(args) == 1:

        if not os.path.exists(args[0]):
            sys.exit('ERROR: Configuration file %s not found!' % args[0])

        config = json.load(open(args[0]))
    else:
        config = {
            "hub":{
                "host":options.hub_host,
                "port":options.hub_port},
            "nodes":[{
                "host":options.node_host,
                "port":options.node_port,
                "browser": {
                    "name":options.browser_name,
                    "version":options.browser_version},
                "platform":options.platform}]}

    hub_host = config['hub']['host']
    hub_port = config['hub']['port']

    for node in config['nodes']:
        node_id = node.get('id', 'http://%s:%s' % (node['host'], node['port']))
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

        status = 'Registering %s:%s to %s:%s' % (
            node_host,
            node_port,
            hub_host,
            hub_port)
        print status,

        proxy_registered = False
        try:
            url = 'http://%s:%i/grid/api/proxy?id=%s' % (hub_host, hub_port, node_id)
            response = json.load(urllib2.urlopen(urllib2.Request(url)))
            proxy_registered = response.get('success', False)
        except IOError, e:
            print '\r%s [%s]' % (status, colored('FAILED', 'red'))
            if options.verbose:
                print e
            continue

        if proxy_registered and not options.force:
            print '\r%s [%s]' % (status, colored('SKIPPED', 'yellow'))
            if options.verbose:
                print 'Node is already registered.'
        else:
            try:
                register_url = 'http://%s:%i/grid/register' % (hub_host, hub_port)
                urllib2.urlopen(urllib2.Request(register_url, data))
                print '\r%s [%s]' % (status, colored('SUCCESS', 'green'))
            except IOError, e:
                print '\r%s [%s]' % (status, colored('FAILED', 'red'))
                if options.verbose:
                    print e


if __name__ == '__main__':
    main()
