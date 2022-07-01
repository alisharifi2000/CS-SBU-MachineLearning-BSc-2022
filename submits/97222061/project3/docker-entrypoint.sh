#!/usr/bin/env bash

echo "Starting Gunicorn..."
exec gunicorn machine_learning.wsgi:application -c gunicorn.py
