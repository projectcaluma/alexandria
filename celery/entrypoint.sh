#!/bin/sh

wait-for-it db:5432 -- wait-for-it redis:6379;

if [ "$ENV" = "dev" ]; then
    watchmedo auto-restart -d . --recursive -p '*.py' -- celery -A alexandria worker -l INFO -E -O fair;
else
    celery -A alexandria worker -l INFO -E -O fair;
fi
