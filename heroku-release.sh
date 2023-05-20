cd app
ls -la
python manage.py collectstatic --noinput
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
