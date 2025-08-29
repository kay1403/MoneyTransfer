#!/bin/bash

# Appliquer les migrations à chaque déploiement
python manage.py migrate --noinput

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer l’app avec gunicorn
gunicorn MoneyTransfer.wsgi:application --bind 0.0.0.0:$PORT
