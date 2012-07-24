#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from optparse import OptionParser
import json
import urllib2

def main ():
    parser = OptionParser(version='%prog 0.2')
    parser.set_defaults(verbose=False)
    parser.add_option('-v', '--verbose',
                      action='store_true',
                      help='increase verbosity')
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
    
    url = 'http://%s:%i/grid/register' % (options.hub_host, options.hub_port)

    nodes = []
    if options.node_config:
        f = open(options.node_config)
        nodes.extend(json.load(f))
    else:
        if not options.browser_name:
            raise Exception('--browsername must be specified!')
        if not options.browser_version:
            raise Exception('--browserver must be specified!')
        if not options.platform:
            raise Exception('--platform must be specified!')
        nodes.append({
            'host':options.node_host,
            'port':options.node_port,
            'browser':{
                'name':options.browser_name,
                'version':options.browser_version
            },
            'platform':options.platform
        })

    for node in nodes:
        data = {
            'class': 'org.openqa.grid.common.RegistrationRequest',
            'capabilities': [{
                'seleniumProtocol': 'WebDriver',
                'browserName': node['browser']['name'],
                'version': node['browser']['version'],
                'platform': node['platform'],
                'maxInstances': 1}],
            'configuration': {
                'port': node['port'],
                'host': node['host'],
                'proxy': 'org.openqa.grid.selenium.proxy.DefaultRemoteProxy',
                'register': True,
                'registerCycle': 5000,
                'hubHost': options.hub_host,
                'hub': 'http://%s:%i/grid/register' % (options.hub_host, options.hub_port),
                'url': 'http://%s:%i' % (node['host'], node['port']),
                'remoteHost': 'http://%s:%i' % (node['host'], node['port']),
                'maxSession': 1,
                'role': 'node',
                'hubPort': options.hub_port}}
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
