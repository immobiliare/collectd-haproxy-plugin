#!/bin/bash
set -euo pipefail
pycodestyle --max-line-length=120 haproxy.py
py.test test_haproxy.py
