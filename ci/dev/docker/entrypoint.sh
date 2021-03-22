#!/usr/bin/env sh

set -e

DB_HOST=`echo ${DATABASE_URL} | sed -r 's/.*@([^:]+):.*/\1/'`
DB_PORT=`echo ${DATABASE_URL} | sed -e 's,^.*:,:,g' -e 's,.*:\([0-9]*\).*,\1,g' -e 's,[^0-9],,g'`
dockerize -wait tcp://${DB_HOST}:${DB_PORT}

# Миграция и синхронизация
./manage.py migrate --noinput
./manage.py loaddata crm/fixtures/dev.json
#./manage.py collectstatic --noinput
#./manage.py sync_permissions
#./manage.py sync_db

# Запуск команды
./manage.py runserver 0.0.0.0:8000
