# mkdir feesprefect/static
python manage.py collectstatic --noinput
ls -la
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
