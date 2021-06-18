#!/usr/bin/env python
#
# Copyright (c) 2020 Immobiliare Labs <opensource@immobiliare.it>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function

import collections
import sys

from mock import call
from mock import MagicMock
from mock import Mock
from mock import patch


class MockCollectd(MagicMock):
    """
    Mocks the functions and objects provided by the collectd module
    """

    @staticmethod
    def log(log_str):
        print(log_str)

    debug = log
    info = log
    warning = log
    error = log


class MockHAProxySocketSimple:
    def __init__(self, sockets=["whatever"]):
        self.sockets = sockets

    def get_resolvers(self):
        return {}

    def get_server_info(self):
        return {
            'ConnRate': '3',
            'CumReq': '5',
            'Idle_pct': '78'
        }

    def get_server_stats(self):
        return [{
            'bin': '3120628',
            'lastchg': '',
            'lbt': '',
            'weight': '',
            'wretr': '',
            'slim': '50',
            'pid': '1',
            'wredis': '',
            'dresp': '0',
            'ereq': '0',
            'pxname': 'sample_proxy',
            'stot': '39728',
            'sid': '0',
            'bout': '188112702395',
            'qlimit': '',
            'status': 'OPEN',
            'smax': '2',
            'dreq': '0',
            'econ': '',
            'iid': '2',
            'chkfail': '',
            'downtime': '',
            'qcur': '',
            'eresp': '',
            'throttle': '',
            'scur': '0',
            'bck': '',
            'qmax': '',
            'act': '',
            'chkdown': '',
            'svname': 'FRONTEND'
        }]


class MockHAProxySocketComplex:
    def __init__(self, socket_file="whatever"):
        self.socket_file = socket_file

    def get_resolvers(self):
        return {
            'dns1': {
                'sent': '8',
                'snd_error': '0',
                'valid': '4',
                'update': '0',
                'cname': '0',
                'cname_error': '4',
                'any_err': '0',
                'nx': '0',
                'timeout': '0',
                'refused': '0',
                'other': '0',
                'invalid': '0',
                'too_big': '0',
                'truncated': '0',
                'outdated': '0'
            }, 'dns2': {
                'sent': '0',
                'snd_error': '0',
                'valid': '0',
                'update': '0',
                'cname': '0',
                'cname_error': '0',
                'any_err': '0',
                'nx': '0',
                'timeout': '0',
                'refused': '0',
                'other': '0',
                'invalid': '0',
                'too_big': '0',
                'truncated': '0',
                'outdated': '0'
            }
        }

    def get_server_info(self):
        return {
            'ConnRate': '3',
            'CumReq': '5',
            'Idle_pct': '78'
        }

    def get_server_stats(self):
        return [{
            'lastchg': '321093',
            'agent_health': '',
            'check_desc': 'Layer7 check passed',
            'smax': '2',
            'agent_rise': '',
            'req_rate': '',
            'check_status': 'L7OK',
            'wredis': '0',
            'comp_out': '',
            'conn_rate': '',
            'cli_abrt': '0',
            'pxname': 'elasticsearch_backend',
            'check_code': '0',
            'check_health': '4',
            'check_fall': '3',
            'qlimit': '',
            'bin': '0',
            'conn_rate_max': '',
            'hrsp_5xx': '',
            'stot': '344777',
            'econ': '0',
            'iid': '3',
            'hrsp_4xx': '',
            'hanafail': '',
            'downtime': '0',
            'eresp': '0',
            'bout': '0',
            'dses': '',
            'qtime': '0',
            'srv_abrt': '0',
            'throttle': '',
            'ctime': '0',
            'scur': '0',
            'type': '2',
            'check_rise': '2',
            'intercepted': '',
            'hrsp_2xx': '',
            'mode': 'tcp',
            'agent_code': '',
            'qmax': '0',
            'agent_desc': '',
            'weight': '1',
            'slim': '',
            'pid': '1',
            'comp_byp': '',
            'lastsess': '0',
            'comp_rsp': '',
            'agent_status': '',
            'check_duration': '0',
            'rate': '2',
            'rate_max': '9',
            'dresp': '0',
            'ereq': '',
            'addr': '192.168.1.1:6379',
            'comp_in': '',
            'dcon': '',
            'last_chk': '(tcp-check)',
            'sid': '1',
            'ttime': '18',
            'hrsp_1xx': '',
            'agent_duration': '',
            'hrsp_other': '',
            'status': 'UP',
            'wretr': '0',
            'lbtot': '344777',
            'dreq': '',
            'req_rate_max': '',
            'conn_tot': '',
            'chkfail': '0',
            'cookie': '',
            'qcur': '0',
            'tracked': '',
            'rtime': '0',
            'last_agt': '',
            'bck': '0',
            'req_tot': '',
            'rate_lim': '',
            'hrsp_3xx': '',
            'algo': '',
            'act': '1',
            'chkdown': '0',
            'svname': 'elasticache',
            'agent_fall': ''
        }, {
            'lastchg': '321093',
            'agent_health': '',
            'check_desc': '',
            'smax': '2',
            'agent_rise': '',
            'req_rate': '',
            'check_status': '',
            'wredis': '0',
            'comp_out': '0',
            'conn_rate': '',
            'cli_abrt': '0',
            'pxname': 'elasticsearch_backend',
            'check_code': '',
            'check_health': '',
            'check_fall': '',
            'qlimit': '',
            'bin': '0',
            'conn_rate_max': '',
            'hrsp_5xx': '',
            'stot': '515751',
            'econ': '0',
            'iid': '3',
            'hrsp_4xx': '',
            'hanafail': '',
            'downtime': '0',
            'eresp': '0',
            'bout': '0',
            'dses': '',
            'qtime': '0',
            'srv_abrt': '0',
            'throttle': '',
            'ctime': '0',
            'scur': '0',
            'type': '1',
            'check_rise': '',
            'intercepted': '',
            'hrsp_2xx': '',
            'mode': 'tcp',
            'agent_code': '',
            'qmax': '0',
            'agent_desc': '',
            'weight': '1',
            'slim': '800',
            'pid': '1',
            'comp_byp': '0',
            'lastsess': '0',
            'comp_rsp': '0',
            'agent_status': '',
            'check_duration': '',
            'rate': '3',
            'rate_max': '9',
            'dresp': '0',
            'ereq': '',
            'addr': '',
            'comp_in': '0',
            'dcon': '',
            'last_chk': '',
            'sid': '0',
            'ttime': '18',
            'hrsp_1xx': '',
            'agent_duration': '',
            'hrsp_other': '',
            'status': 'UP',
            'wretr': '0',
            'lbtot': '344777',
            'dreq': '0',
            'req_rate_max': '',
            'conn_tot': '',
            'chkfail': '',
            'cookie': '',
            'qcur': '0',
            'tracked': '',
            'rtime': '0',
            'last_agt': '',
            'bck': '0',
            'req_tot': '',
            'rate_lim': '',
            'hrsp_3xx': '',
            'algo': 'roundrobin',
            'act': '1',
            'chkdown': '0',
            'svname': 'BACKEND',
            'agent_fall': ''
        }, {
            'lastchg': '',
            'agent_health': None,
            'check_desc': None,
            'smax': '0',
            'agent_rise': None,
            'req_rate': '0',
            'check_status': '',
            'wredis': '',
            'comp_out': None,
            'conn_rate': None,
            'cli_abrt': None,
            'pxname': 'sensu_frontend',
            'check_code': '',
            'check_health': None,
            'check_fall': None,
            'qlimit': '',
            'bin': '0',
            'conn_rate_max': None,
            'hrsp_5xx': '',
            'stot': '0',
            'econ': '',
            'iid': '4',
            'hrsp_4xx': '',
            'hanafail': '',
            'downtime': '',
            'eresp': '',
            'bout': '0',
            'dses': None,
            'qtime': None,
            'srv_abrt': None,
            'throttle': '',
            'ctime': None,
            'scur': '0',
            'type': '0',
            'check_rise': None,
            'intercepted': None,
            'hrsp_2xx': '',
            'mode': None,
            'agent_code': None,
            'qmax': '',
            'agent_desc': None,
            'weight': '',
            'slim': '8000',
            'pid': '1',
            'comp_byp': None,
            'lastsess': None,
            'comp_rsp': None,
            'agent_status': None,
            'check_duration': '',
            'rate': '0',
            'rate_max': '10',
            'dresp': '0',
            'ereq': '0',
            'addr': None,
            'comp_in': None,
            'dcon': None,
            'last_chk': None,
            'sid': '0',
            'ttime': None,
            'hrsp_1xx': '',
            'agent_duration': None,
            'hrsp_other': '',
            'status': 'OPEN',
            'wretr': '',
            'lbtot': '',
            'dreq': '0',
            'req_rate_max': '0',
            'conn_tot': None,
            'chkfail': '',
            'cookie': None,
            'qcur': '',
            'tracked': '',
            'rtime': None,
            'last_agt': None,
            'bck': '',
            'req_tot': '',
            'rate_lim': '0',
            'hrsp_3xx': '',
            'algo': None,
            'act': '',
            'chkdown': '',
            'svname': 'FRONTEND',
        }]


# don't move the block below
sys.modules['collectd'] = MockCollectd()
import haproxy  # nopep8
ConfigOption = collections.namedtuple('ConfigOption', ('key', 'values'))
mock_config_default_values = Mock()
mock_config_default_values.children = [
    ConfigOption('Testing', ('True',))
]


def test_default_config():
    module_config = haproxy.config(mock_config_default_values)
    assert module_config['sockets'] == ['/var/run/haproxy.sock']
    assert module_config['proxy_monitors'] == ['server', 'frontend', 'backend']
    assert module_config['testing']


@patch('haproxy.HAProxySocket', MockHAProxySocketComplex)
def test_metrics_submitted_for_frontend_with_correct_names():
    haproxy.submit_metrics = MagicMock()
    mock_config = Mock()
    mock_config.children = [
        ConfigOption('ProxyMonitor', ('frontend',)),
        ConfigOption('EnhancedMetrics', ('True',)),
        ConfigOption('Testing', ('True',))
    ]
    haproxy.collect_metrics(haproxy.config(mock_config))
    haproxy.submit_metrics.assert_has_calls([
        call({
            'values': (3,),
            'type_instance': 'connrate',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (5,),
            'type_instance': 'cumreq',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (78,),
            'type_instance': 'idle_pct',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'smax',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'rate',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'req_rate',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'dresp',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'ereq',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'dreq',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'bin',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'stot',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'req_rate_max',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (8000,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'slim',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'rate_lim',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'bout',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'scur',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (10,),
            'plugin_instance': 'frontend.sensu_frontend',
            'type_instance': 'rate_max',
            'type': 'gauge',
            'plugin': 'haproxy'
        })
    ], any_order=True)


@patch('haproxy.HAProxySocket', MockHAProxySocketComplex)
def test_metrics_submitted_for_backend_and_server_with_correct_names():
    haproxy.submit_metrics = MagicMock()
    mock_config = Mock()
    mock_config.children = [
        ConfigOption('ProxyMonitor', ('backend',)),
        ConfigOption('EnhancedMetrics', ('True',)),
        ConfigOption('Testing', ('True',))
    ]
    haproxy.collect_metrics(haproxy.config(mock_config))
    haproxy.submit_metrics.assert_has_calls([
        call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'rtime',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (2,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'smax',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'lastsess',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'check_duration',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (2,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'rate',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'wredis',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'eresp',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'dresp',
            'type': 'derive',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'cli_abrt',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'bin',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (344777,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'lbtot',
            'type': 'counter',
            'plugin': 'haproxy'
        }), call({
            'values': (344777,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'stot',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'econ',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (18,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'ttime',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'downtime',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'qcur',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'wretr',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'qtime',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'srv_abrt',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'bout',
            'type': 'derive',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'ctime',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'scur',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'bck',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'qmax',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (9,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'rate_max',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (1,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'act',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend.elasticache',
            'type_instance': 'chkfail',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'rtime',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (2,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'smax',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'comp_byp',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'lastsess',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (3,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'rate',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'wredis',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'comp_out',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'eresp',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'dresp',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'comp_in',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'dreq',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'cli_abrt',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'bin',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (344777,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'lbtot',
            'type': 'counter',
            'plugin': 'haproxy'
        }), call({
            'values': (515751,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'stot',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'econ',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (18,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'ttime',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (800,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'slim',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'downtime',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'qcur',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'comp_rsp',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'wretr',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'qtime',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'srv_abrt',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'bout',
            'type': 'derive',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'ctime',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'scur',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'bck',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'qmax',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (9,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'rate_max',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (1,),
            'plugin_instance': 'backend.elasticsearch_backend',
            'type_instance': 'act',
            'type': 'gauge',
            'plugin': 'haproxy'
        })
    ], any_order=True)


@patch('haproxy.HAProxySocket', MockHAProxySocketComplex)
def test_metrics_submitted_for_resolvers():
    haproxy.submit_metrics = MagicMock()
    mock_config = Mock()
    mock_config.children = [
        ConfigOption('Testing', ('True',))
    ]
    haproxy.collect_metrics(haproxy.config(mock_config))
    haproxy.submit_metrics.assert_has_calls([
        call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'cname_error',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'truncated',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'update',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'refused',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'any_err',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'cname',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'outdated',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'too_big',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'invalid',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'snd_error',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'nx',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'valid',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'timeout',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'other',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns2',
            'type_instance': 'sent',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (4,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'cname_error',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'truncated',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'update',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'refused',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'any_err',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance':
            'cname',
                'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'outdated',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'too_big',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'invalid',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'snd_error',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'nx',
            'type': 'gauge',
                    'plugin': 'haproxy'
        }), call({
            'values': (4,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'valid',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'timeout',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (0,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'other',
            'type': 'gauge',
            'plugin': 'haproxy'
        }), call({
            'values': (8,),
            'plugin_instance': 'nameserver.dns1',
            'type_instance': 'sent',
            'type': 'gauge',
            'plugin': 'haproxy'
        })
    ], any_order=True)


def test_resolver_stats_can_be_parsed():
    haproxy_socket = haproxy.HAProxySocket(MagicMock())
    haproxy_socket.communicate = MagicMock(
        return_value=["""Resolvers section mydns
 nameserver dns1:
  sent:        8
  snd_error:   0
  valid:       4
  update:      0
  cname:       0
  cname_error: 4
  any_err:     0
  nx:          0
  timeout:     0
  refused:     0
  other:       0
  invalid:     0
  too_big:     0
  truncated:   0
  outdated:    0

Resolvers section mydns2
 nameserver dns2:
  sent:        0
  snd_error:   0
  valid:       0
  update:      0
  cname:       0
  cname_error: 0
  any_err:     0
  nx:          0
  timeout:     0
  refused:     0
  other:       0
  invalid:     0
  too_big:     0
  truncated:   0
  outdated:    0"""])
    assert haproxy_socket.get_resolvers() == {
        'dns1': {
            'sent': '8',
            'snd_error': '0',
            'valid': '4',
            'update': '0',
            'cname': '0',
            'cname_error': '4',
            'any_err': '0',
            'nx': '0',
            'timeout': '0',
            'refused': '0',
            'other': '0',
            'invalid': '0',
            'too_big': '0',
            'truncated': '0',
            'outdated': '0'
        }, 'dns2': {
            'sent': '0',
            'snd_error': '0',
            'valid': '0',
            'update': '0',
            'cname': '0',
            'cname_error': '0',
            'any_err': '0',
            'nx': '0',
            'timeout': '0',
            'refused': '0',
            'other': '0',
            'invalid': '0',
            'too_big': '0',
            'truncated': '0',
            'outdated': '0'
        }}
