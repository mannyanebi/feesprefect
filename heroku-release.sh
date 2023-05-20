ls -la
pwd
cd static
pwd
cd ../
mkdir feesprefect/static
python manage.py collectstatic --noinput
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
