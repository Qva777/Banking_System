#!/bin/bash

if [ ! -d "migrations" ]; then
    echo "Initializing migrations"
    flask db init
fi

echo "Applying migrations"
flask db upgrade

echo "run server"
flask run --host=0.0.0.0 --debug