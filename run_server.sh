#!/bin/bash
exec gunicorn celerymonitor.wsgi:application -w 2 -b :8905 --threads 1 --timeout 80