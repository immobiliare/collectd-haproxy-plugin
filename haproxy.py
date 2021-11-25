#!/usr/bin/env python
#
# Author: Michael Leinartas
# Description: This is a collectd plugin which runs under the Python plugin to
# collect metrics from haproxy.
# Plugin structure and logging func taken from
# https://github.com/phrawzty/rabbitmq-collectd-plugin
#
# Modified by:
# - "Warren Turkal" <wt@signalfuse.com>
# - "Volodymyr Zhabiuk" <vzhabiuk@signalfx.com>
# - "HM Revenue & Customs" <hmrc-web-operations@digital.hmrc.gov.uk>
# - "Davide Pucci" <davide.pucci@immobiliare.it>

import collectd
import csv
import re
import socket
import sys

PLUGIN_NAME = 'haproxy'
RECV_SIZE = 1024

METRICS_TO_COLLECT = {
    'CompressBpsIn': 'derive',
    'CompressBpsOut': 'derive',
    'ConnRate': 'gauge',
    'CumConns': 'derive',
    'CumReq': 'derive',
    'CumSslConns': 'derive',
    'CurrConns': 'gauge',
    'CurrSslConns': 'gauge',
    'Idle_pct': 'gauge',
    'MaxConn': 'gauge',
    'MaxConnRate': 'gauge',
    'MaxPipes': 'gauge',
    'MaxSessRate': 'gauge',
    'MaxSslConns': 'gauge',
    'PipesFree': 'gauge',
    'PipesUsed': 'gauge',
    'Run_queue': 'gauge',
    'SessRate': 'gauge',
    'SslBackendKeyRate': 'gauge',
    'SslCacheLookups': 'derive',
    'SslCacheMisses': 'derive',
    'SslFrontendKeyRate': 'gauge',
    'SslRate': 'gauge',
    'Tasks': 'gauge',
    'Uptime_sec': 'derive',
    'ZlibMemUsage': 'gauge',
    'act': 'gauge',
    'any_err': 'gauge',
    'bck': 'gauge',
    'bin': 'derive',
    'bout': 'derive',
    'check_duration': 'gauge',
    'chkfail': 'derive',
    'cli_abrt': 'derive',
    'cname': 'gauge',
    'cname_error': 'gauge',
    'comp_byp': 'derive',
    'comp_in': 'derive',
    'comp_out': 'derive',
    'comp_rsp': 'derive',
    'conn_rate': 'gauge',
    'conn_rate_max': 'gauge',
    'conn_tot': 'counter',
    'ctime': 'gauge',
    'dcon': 'gauge',
    'downtime': 'derive',
    'dreq': 'derive',
    'dresp': 'derive',
    'dses': 'gauge',
    'econ': 'derive',
    'ereq': 'derive',
    'eresp': 'derive',
    'hrsp_1xx': 'derive',
    'hrsp_2xx': 'derive',
    'hrsp_3xx': 'derive',
    'hrsp_4xx': 'derive',
    'hrsp_5xx': 'derive',
    'hrsp_other': 'derive',
    'intercepted': 'gauge',
    'invalid': 'gauge',
    'lastsess': 'gauge',
    'lbtot': 'counter',
    'nx': 'gauge',
    'other': 'gauge',
    'outdated': 'gauge',
    'qcur': 'gauge',
    'qlimit': 'gauge',
    'qmax': 'gauge',
    'qtime': 'gauge',
    'rate': 'gauge',
    'rate_lim': 'gauge',
    'rate_max': 'gauge',
    'refused': 'gauge',
    'req_rate': 'gauge',
    'req_rate_max': 'gauge',
    'rtime': 'gauge',
    'scur': 'gauge',
    'sent': 'gauge',
    'slim': 'gauge',
    'smax': 'gauge',
    'snd_error': 'gauge',
    'srv_abrt': 'derive',
    'stot': 'derive',
    'throttle': 'gauge',
    'timeout': 'gauge',
    'too_big': 'gauge',
    'truncated': 'gauge',
    'ttime': 'gauge',
    'update': 'gauge',
    'valid': 'gauge',
    'wredis': 'derive',
    'wretr': 'derive',
}

# svname, pxname, type are absolutely mandatory
# here to keep the overall plugin flow working
METRICS_AGGR_PULL = [
    'pxname',
    'svname',
    'type',
]
METRICS_AGGR_SUM = [
    'CompressBpsIn',
    'CompressBpsOut',
    'CumConns',
    'CumReq',
    'CumSslConns',
    'CurrConns',
    'CurrSslConns',
    'Idle_pct',
    'MaxConn',
    'MaxPipes',
    'MaxSslConns',
    'PipesFree',
    'PipesUsed',
    'Run_queue',
    'SslCacheMisses',
    'Tasks',
    'act',
    'any_err',
    'bck',
    'bin',
    'bout',
    'check_duration',
    'chkfail',
    'cli_abrt',
    'cname',
    'cname_error',
    'comp_byp',
    'comp_in',
    'comp_out',
    'comp_rsp',
    'conn_tot',
    'dcon',
    'dreq',
    'dresp',
    'dses',
    'econ',
    'ereq',
    'eresp',
    'hrsp_1xx',
    'hrsp_2xx',
    'hrsp_3xx',
    'hrsp_4xx',
    'hrsp_5xx',
    'hrsp_other',
    'intercepted',
    'invalid',
    'lastsess',
    'lbtot',
    'nx',
    'other',
    'outdated',
    'qcur',
    'refused',
    'scur',
    'sent',
    'slim',
    'snd_error',
    'srv_abrt',
    'stot',
    'throttle',
    'timeout',
    'too_big',
    'truncated',
    'update',
    'valid',
    'wredis',
    'wretr',
]
METRICS_AGGR_MEAN = [
    'ConnRate',
    'MaxConnRate',
    'MaxSessRate',
    'SessRate',
    'SslBackendKeyRate',
    'SslCacheLookups',
    'SslFrontendKeyRate',
    'SslRate',
    'Uptime_sec',
    'ZlibMemUsage',
    'conn_rate',
    'conn_rate_max',
    'ctime',
    'downtime',
    'qlimit',
    'qmax',
    'qtime',
    'rate',
    'rate_lim',
    'rate_max',
    'req_rate',
    'req_rate_max',
    'rtime',
    'smax',
    'ttime',
]

DEFAULT_SOCKET = '/var/run/haproxy.sock'
DEFAULT_PROXY_MONITORS = ['server', 'frontend', 'backend']


class HAProxySocket(object):
    '''
    Encapsulates communication with HAProxy via the socket interface
    '''

    def __init__(self, socket_files=[DEFAULT_SOCKET]):
        self.sockets = socket_files
        # for socket in socket_files:
        #     self.sockets[socket] = None

    def communicate(self, command):
        '''
        Get response from single command.

        Args:
            command: string command to send to haproxy stat socket

        Returns:
            a string of the response data
        '''
        if not command.endswith('\n'):
            command += '\n'

        outputs = []
        for socket in self.sockets:
            conn = HAProxySocket._connect(socket)
            if conn is None:
                collectd.warning('unable to connect to {}'.format(socket))
                continue

            if sys.version_info[0] >= 3:
                command = command.encode('utf-8')
            conn.sendall(command)
            result_buf = str()
            buf = conn.recv(RECV_SIZE)
            while buf:
                result_buf += str(buf.decode('utf-8'))
                buf = conn.recv(RECV_SIZE)

            conn.close()
            outputs.append(result_buf)

        return outputs

    # this method isn't nice but there's no other way
    # to parse the output of show resolvers from haproxy
    def get_resolvers(self):
        '''
        Gets the resolver config and return s,
        whish is a map of nameserver -> nameservermetrics.

        The output from the socket looks like
        Resolvers section mydns
         nameserver dns1:
          sent:        8
          ...

        :return:
        map of nameserver -> nameservermetrics
        e.g. '{dns1': {'sent': '8', ...}, ...}
        '''
        result = {}
        sockets_stats = self.communicate('show resolvers')
        nameserver = None

        for stats in sockets_stats:
            lines = stats.splitlines()
            # check if command is supported
            if any(lines) and lines[0].lower().startswith('unknown command'):
                continue

            for line in lines:
                try:
                    if 'Resolvers section' in line or line.strip() == '':
                        continue
                    elif 'nameserver' in line:
                        _, unsanitied_nameserver = line.strip().split(' ', 1)
                        # remove trailing ':'
                        nameserver = unsanitied_nameserver[:-1]
                        result[nameserver] = {}
                    elif nameserver:
                        key, val = line.split(':', 1)
                        current_nameserver_stats = result[nameserver]
                        current_nameserver_stats[key.strip()] = val.strip()
                        result[nameserver] = current_nameserver_stats
                except ValueError:
                    continue

        return result

    def get_server_info(self):
        result = {}
        sockets_stats = self.communicate('show info')

        for stats in sockets_stats:
            stats_proc = self.get_server_info_proc_num(stats)

            for line in stats.splitlines():
                try:
                    key, val = line.split(':', 1)
                except ValueError:
                    continue
                result['{}#{}'.format(key.strip(), stats_proc)] = val.strip()

        return result

    def get_server_info_proc_num(self, data):
        for _, match in enumerate(
                re.finditer(r'Process_num: ([0-9]+)', data, re.MULTILINE),
                start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                return match.group(groupNum).strip()
        return 'U'

    def get_server_stats(self):
        result = []
        sockets_stats = self.communicate('show stat')
        for stat in sockets_stats:
            # sanitize and make a list of lines
            output = stat.lstrip('# ').strip()
            output = [line.strip(',') for line in output.splitlines()]
            csvreader = csv.DictReader(output)
            result += [d.copy() for d in csvreader]

        return HAProxySocket._aggregate(result)

    @staticmethod
    def _aggregate(stats):
        aggregate = {}

        for stat in stats:
            aggr_key = _format_plugin_instance(stat)
            if aggr_key not in aggregate:
                aggregate[aggr_key] = {}

            for key in set(aggregate[aggr_key]) | set(stat):
                val_left = aggregate[aggr_key].get(key, 0)
                val_right = stat.get(key, '0')
                if key in METRICS_AGGR_PULL:
                    aggregate[aggr_key][key] = val_right
                elif key in METRICS_AGGR_SUM:
                    if not val_right or not val_right.isdigit():
                        continue
                    aggregate[aggr_key][key] = val_left + int(val_right)
                elif key in METRICS_AGGR_MEAN:
                    if not val_right or not val_right.isdigit():
                        continue
                    key_aggr_mean_label = '{}_aggr_mean_cnt'.format(key)
                    if key_aggr_mean_label not in aggregate[aggr_key]:
                        aggregate[aggr_key][key_aggr_mean_label] = 0

                    aggregate[aggr_key][key_aggr_mean_label] = \
                        aggregate[aggr_key][key_aggr_mean_label] + 1
                    # compute a progressive mean as we don't know
                    # how many elements to do the calculation for apriori.
                    # this way, at any step the calculation is computed,
                    # it represents a perfectly valid mean.
                    nxt_mean_cnt = aggregate[aggr_key][key_aggr_mean_label]
                    crr_mean_cnt = aggregate[aggr_key][key_aggr_mean_label] - 1
                    aggregate[aggr_key][key] = \
                        ((val_left * crr_mean_cnt) + int(val_right)) \
                        / nxt_mean_cnt
                else:
                    pass

        return list(aggregate.values())

    @staticmethod
    def _connect(payload):
        if payload.startswith('file://') \
            or payload.startswith('unix://') \
                or payload.startswith('/'):
            fname = payload.replace('file://', '').replace('unix://', '')
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(fname)
            return sock
        elif payload.startswith('tcp://'):
            host, port = payload.replace('tcp://', '').split(':')
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, int(port)))
            return sock
        elif payload.startswith('http://'):
            pass

        collectd.warning('{} socket type not recognized'.format(payload))
        return None


def get_stats(module_config):
    '''
    Makes two calls to haproxy to fetch server info and server stats.
    Returns the dict containing metric name as the key
    and a tuple of metric value and the dict of dimensions if any.
    '''
    if 'sockets' not in module_config or len(module_config['sockets']) == 0:
        collectd.error(
            "At least a socket must be given as a configuration parameter")
        return

    stats = []
    haproxy = HAProxySocket(module_config['sockets'])

    try:
        server_info = haproxy.get_server_info()
        server_stats = haproxy.get_server_stats()
        resolver_stats = haproxy.get_resolvers()
    except socket.error as e:
        collectd.warning(
            'unable to connect to the HAProxy socket: {}'.format(str(e)))
        return stats

    # server wide stats
    for key, val in server_info.items():
        try:
            stats.append((key, int(val), dict()))
        except (TypeError, ValueError):
            pass

    # proxy specific stats
    for statdict in server_stats:
        if not should_capture_metric(statdict, module_config):
            continue
        for metricname, val in statdict.items():
            try:
                stats.append((metricname, int(val), statdict))
            except (TypeError, ValueError):
                pass

    for resolver, resolver_stats in resolver_stats.items():
        for metricname, val in resolver_stats.items():
            try:
                stats.append((metricname, int(val), {
                    'is_resolver': True,
                    'nameserver': resolver
                }))
            except (TypeError, ValueError):
                pass

    return stats


def should_capture_metric(statdict, module_config):
    return (
        (
            'svname' in statdict and
            statdict['svname'].lower() in module_config['proxy_monitors']
        ) or (
            'pxname' in statdict and
            statdict['pxname'].lower() in module_config['proxy_monitors']
        ) or is_backend_server_metric(statdict) and
        'backend' in module_config['proxy_monitors']
    )


def is_backend_server_metric(statdict):
    return 'type' in statdict and _get_proxy_type(statdict['type']) == 'server'


def is_resolver_metric(statdict):
    return 'is_resolver' in statdict and statdict['is_resolver']


def config(config_values):
    '''
    A callback method that loads information
    from the HaProxy collectd plugin config file.

    Args:
    config_values (collectd.Config): Object containing config values
    '''

    module_config = {}
    sockets = []
    proxy_monitors = []
    excluded_metrics = set()
    enhanced_metrics = False
    interval = None
    testing = False
    custom_dimensions = {}

    for node in config_values.children:
        if node.key == "ProxyMonitor" and node.values[0]:
            proxy_monitors.extend(node.values)
        elif node.key == "Socket" and node.values:
            sockets.extend(node.values)
        elif node.key == "Interval" and node.values[0]:
            interval = node.values[0]
        elif node.key == "Testing" and node.values[0]:
            testing = _str_to_bool(node.values[0])
        elif node.key == 'Dimension':
            if len(node.values) == 2:
                custom_dimensions.update({node.values[0]: node.values[1]})
            else:
                collectd.warning("WARNING: Check configuration \
                                            setting for %s" % node.key)
        else:
            collectd.warning('Unknown config key: %s' % node.key)

    if not sockets:
        sockets.append(DEFAULT_SOCKET)
    if not proxy_monitors:
        proxy_monitors += DEFAULT_PROXY_MONITORS

    module_config = {
        'sockets': sockets,
        'proxy_monitors': proxy_monitors,
        'interval': interval,
        'enhanced_metrics': enhanced_metrics,
        'excluded_metrics': excluded_metrics,
        'custom_dimensions': custom_dimensions,
        'testing': testing,
    }

    if testing:
        return module_config

    # pass interval only if not None
    interval_kwarg = {}
    if interval:
        interval_kwarg['interval'] = interval

    collectd.register_read(
        collect_metrics, data=module_config,
        name='node_{}_{}'.format('_'.join(sockets), '_'.join(proxy_monitors)),
        **interval_kwarg)


def _format_plugin_instance(dimensions):
    if is_backend_server_metric(dimensions):
        return "{0}.{1}.{2}".format(
            "backend",
            dimensions['pxname'].lower(),
            dimensions['svname']
        )
    elif is_resolver_metric(dimensions):
        return "nameserver.{0}".format(
            dimensions['nameserver']
        )
    else:
        return "{0}.{1}".format(
            dimensions['svname'].lower(),
            dimensions['pxname']
        )


def _get_proxy_type(type_id):
    '''
    Return human readable proxy type
    '''
    return {
        0: 'frontend',
        1: 'backend',
        2: 'server',
        3: 'socket/listener',
    }.get(int(type_id))


def _str_to_bool(val):
    '''
    Converts a true/false string to a boolean
    '''
    val = str(val).strip().lower()
    if val == 'true':
        return True
    elif val != 'false':
        collectd.warning(
            '"%s" cannot be converted to a bool: returning false.' % val)

    return False


def submit_metrics(metric_datapoint):
    datapoint = collectd.Values()
    datapoint.type = metric_datapoint['type']
    datapoint.type_instance = metric_datapoint['type_instance']
    datapoint.plugin = metric_datapoint['plugin']
    if 'plugin_instance' in metric_datapoint.keys():
        datapoint.plugin_instance = metric_datapoint['plugin_instance']
    datapoint.values = metric_datapoint['values']
    datapoint.dispatch()


def collect_metrics(module_config):
    '''
    A callback method that gets metrics from HAProxy
    and records them to collectd.
    '''

    collectd.debug('beginning collect_metrics')
    info = get_stats(module_config)

    if not info:
        collectd.warning('%s: No data received' % PLUGIN_NAME)
        return

    for metric_name, metric_value, dimensions in info:
        # assert metric is in valid metrics lists
        if metric_name not in METRICS_TO_COLLECT:
            collectd.debug(
                "metric %s is ignored" % metric_name.lower())
            continue

        metric_datapoint = {
            'plugin': PLUGIN_NAME,
            'type': METRICS_TO_COLLECT[metric_name],
            'type_instance': metric_name.lower(),
            'values': (metric_value,)
        }
        if len(dimensions) > 0:
            metric_datapoint['plugin_instance'] = _format_plugin_instance(
                dimensions)
        submit_metrics(metric_datapoint)


collectd.register_config(config)
