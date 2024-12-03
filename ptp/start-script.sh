#!/bin/bash

sh -c /app/start-django.sh
supervisord -c /etc/supervisor/conf.d/supervisord.conf
