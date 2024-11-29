#!/bin/bash
echo "downloading models.."
sh -c /app/download.sh
echo "done!"
echo "starting serving..."

sh -c /app/start-django.sh
supervisord -c /etc/supervisor/conf.d/supervisord.conf
