# Collectd HAProxy plugin <a href="#collectd-haproxy-plugin"><img align="left" width="100px" src="https://github.com/immobiliare/collectd-haproxy-plugin/blob/master/.github/collectd.png"></a>

[![pipeline status](https://github.com/immobiliare/collectd-haproxy-plugin/actions/workflows/test.yml/badge.svg)](https://github.com/immobiliare/collectd-haproxy-plugin/actions/workflows/test.yml)

This is a [collectd](https://collectd.org) plugin for [HAProxy](https://haproxy.com).

It uses the exposed HAProxy socket commands (on defined TCP/Unix sockets) to monitor statistics from the `show info`, `show stat` and `show resolvers` (if on HAProxy 1.8+) commands.
This allows monitoring of the overall service status as well as frontends, backends, servers and resolvers configured.
It also supports multi-process statistics aggregation, allowing to configure multiple sockets to collect metrics from.

It's the result of the [hmrc/collectd-haproxy](https://github.com/hmrc/collectd-haproxy) repository fork, to which, mainly, the support for multi stats sockets aggregation has been added. 

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Compatibility](#compatibility)
- [Requirements](#requirements)
- [Changelog](#changelog)
- [Contributing](#contributing)
- [Issues](#issues)

## Install

Download the latest release of `haproxy.py` file into an arbirtrary path `/usr/local/lib/collectd`, e.g. for version 0.1.0:

```bash
curl -Lo /usr/local/lib/collectd/haproxy.py --create-dirs \
  https://github.com/immobiliare/collectd-haproxy-plugin/releases/download/0.1.0/haproxy.py
```

## Usage

Enabling the plugin follows the widely known standard collectd's way.

```bash
cat <<EOF > /etc/collectd/plugins/haproxy.conf
<LoadPlugin python>
  Globals true
</LoadPlugin>

<Plugin python>
  ModulePath "/usr/local/lib/collectd"
  Import "haproxy"
  <Module haproxy>
    Socket "/var/run/haproxy/proc1.sock"
    Socket "unix:///var/run/haproxy/proc2.sock"
    Socket "tcp://127.0.0.1:8080"
    ProxyMonitor "backend"
    # ProxyMonitor "server" or "frontend"
    # ProxyIgnore to ignore metrics
    # Verbose to increase verbosity
  </Module>
</Plugin>
EOF
```

## Compatibility

| Version | Status                  | Python compatibility | HAproxy compatibility |
| ------- | ----------------------- | -------------------- | --------------------- |
| 1.x     | maintained but untested | cpython >=2.7        | >=1.8                 |
| 1.x     | maintained and tested   | cpython >=3.7        | >=1.8                 |
| 1.x     | maintained and tested   | pypy >=3.7           | >=1.8                 |

## Requirements

There's no particular requirement other than collectd/HAproxy and Python, as per the matrice above.

## Changelog

See [changelog](./CHANGELOG.md).

## Contributing

See [contributing](./CONTRIBUTING.md).

## Issues

You found a bug or need a new feature? Please <a href="https://github.com/immobiliare/collectd-haproxy-plugin/issues/new" target="_blank">open an issue.</a>
