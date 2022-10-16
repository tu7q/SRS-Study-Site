#!/bin/sh

set -e

cd web
celery -A WebApp worker -l INFO -P gevent
