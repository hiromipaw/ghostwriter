#!/bin/sh
set -e

nginx

su - peer

su - peer -c '/usr/bin/tor'

exec "$@"
