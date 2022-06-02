
web: python manage.py collectstatic --no-input
web: gunicorn core.wsgi
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input