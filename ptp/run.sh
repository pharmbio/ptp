#!/bin/bash
_term() {
  echo "Caught SIGTERM signal!"
  kill -TERM "$child" 2>/dev/null
}
trap _term SIGTERM

echo "Installing all migrations"
python3 manage.py makemigrations
python3 manage.py makemigrations inference
python3 manage.py migrate
python3 manage.py collectstatic --no-input

if [ ${LOAD_FIXTURES} ]; then
    echo "loading extra fixtures data..."
  #python3 manage.py loaddata fixtures/data.json
  #python3 inference/register_tasks.py
fi

if [ -z "${DEBUG}" ]; then
  echo "running in PRODUCTION mode with 4 workers!"

  uvicorn ptp.asgi:application --host 0.0.0.0 --port 8000 --workers 4 &
else

  echo "running in DEBUG mode!"
  python3 manage.py runserver 0.0.0.0:8000 &
fi

child=$!
wait "$child"
