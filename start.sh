#!/bin/bash
# Appliquer migrations avant de démarrer
echo "🚀 Lancement des migrations..."
python manage.py migrate --noinput

# Collecte des fichiers statiques
echo "📦 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Lancer l’application avec Gunicorn
echo "🔥 Démarrage de Gunicorn..."
gunicorn MoneyTransfer.wsgi:application --bind 0.0.0.0:$PORT
