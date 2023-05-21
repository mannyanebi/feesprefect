mkdir feesprefect/static
python manage.py collectstatic --noinput
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
