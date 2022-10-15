#!/bin/sh

set -e

cd web
celery -A WebApp beat
