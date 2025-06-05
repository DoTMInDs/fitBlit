#!/bin/bash

python mysite/manage.py collectstatic --no-input
python mysite/manage.py migrate

if [ "$DJANGO_CREATEUSER" == "1" ]; then 
    python mysite/manage.py createsuperuser --noinput
fi

python mysite/manage.py runserver 0.0.0.0:$PORT