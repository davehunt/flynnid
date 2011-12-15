#!/usr/bin/env python

# ***** BEGIN LICENSE BLOCK *****
# Version: MPL 1.1/GPL 2.0/LGPL 2.1
#
# The contents of this file are subject to the Mozilla Public License Version
# 1.1 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
# http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
# for the specific language governing rights and limitations under the
# License.
#
# The Original Code is Mozilla WebQA Tests.
#
# The Initial Developer of the Original Code is Mozilla.
#
# Portions created by the Initial Developer are Copyright (C) 2011
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
#   Dave Hunt <dhunt@mozilla.com>
#
# Alternatively, the contents of this file may be used under the terms of
# either the GNU General Public License Version 2 or later (the "GPL"), or
# the GNU Lesser General Public License Version 2.1 or later (the "LGPL"),
# in which case the provisions of the GPL or the LGPL are applicable instead
# of those above. If you wish to allow use of your version of this file only
# under the terms of either the GPL or the LGPL, and not to allow others to
# use your version of this file under the terms of the MPL, indicate your
# decision by deleting the provisions above and replace them with the notice
# and other provisions required by the GPL or the LGPL. If you do not delete
# the provisions above, a recipient may use your version of this file under
# the terms of any one of the MPL, the GPL or the LGPL.
#
# ***** END LICENSE BLOCK *****

from optparse import OptionParser
import json
import urllib
import urllib2

def main ():
    parser = OptionParser(version='%prog 0.1')
    parser.set_defaults(verbose=False)
    parser.add_option('-v', '--verbose',
                      action='store_true',
                      help='increase verbosity')
    parser.add_option('--hubhost',
                      action='store',
                      type='string',
                      metavar='STR',
                      dest='hub_host',
                      default='localhost',
                      help='host selenium grid is listening on [default: %default]')
    parser.add_option('--hubport',
                      action='store',
                      type='int',
                      metavar='NUM',
                      dest='hub_port',
                      default=4444,
                      help='port selenium grid is listening on [default: %default]')
    parser.add_option('--nodehost',
                      action='store',
                      type='string',
                      metavar='STR',
                      dest='node_host',
                      default='localhost',
                      help='host selenium node is listening on [default: %default]')
    parser.add_option('--nodeport',
                      action='store',
                      type='int',
                      metavar='NUM',
                      dest='node_port',
                      default=5555,
                      help='port selenium node is listening on [default: %default]')
    parser.add_option('--browsername',
                      action='store',
                      type='str',
                      metavar='STR',
                      dest='browser_name',
                      help='name of browser available on node')
    parser.add_option('--browserver',
                      action='store',
                      type='str',
                      metavar='STR',
                      dest='browser_version',
                      help='version of browser available on node')
    parser.add_option('--platform',
                      action='store',
                      type='str',
                      metavar='STR',
                      help='platform of node')
    (options, args) = parser.parse_args()
    
    url = 'http://%s:%i/grid/register' % (options.hub_host, options.hub_port)
    data = {
        'class': 'org.openqa.grid.common.RegistrationRequest',
        'capabilities': [{
            'seleniumProtocol': 'WebDriver',
            'browserName': options.browser_name,
            'version': options.browser_version,
            'platform': options.platform,
            'maxInstances': 1}],
        'configuration': {
            'port': options.node_port,
            'host': options.node_host,
            'proxy': 'org.openqa.grid.selenium.proxy.DefaultRemoteProxy',
            'register': True,
            'registerCycle': 5000,
            'hubHost': options.hub_host,
            'hub': 'http://%s:%i/grid/register' % (options.hub_host, options.hub_port),
            'url': 'http://%s:%i' % (options.node_host, options.node_port),
            'remoteHost': 'http://%s:%i' % (options.node_host, options.node_port),
            'maxSession': 1,
            'role': 'node',
            'hubPort': options.hub_port}}
    data = json.dumps(data)
    if options.verbose:
        print 'Using JSON request: %s' % data

    print 'Registering the node to hub: %s' % url
    request = urllib2.Request(url, data)
    try:
        response = urllib2.urlopen(request)
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
