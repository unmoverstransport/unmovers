
web: python manage.py
web: gunicorn core.wsgi
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input