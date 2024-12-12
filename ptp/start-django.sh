#!/bin/bash
python3 manage.py makemigrations
python3 manage.py makemigrations inference
python3 manage.py migrate
python3 manage.py collectstatic --no-input
