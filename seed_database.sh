#!/bin/bash

rm db.sqlite3
rm -rf ./scriptapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations scriptapi
python3 manage.py migrate scriptapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

