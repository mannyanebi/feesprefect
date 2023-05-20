echo "Running heroku-release.sh"
cd src
echo "Printing pwd"
pwd
python manage.py collectstatic --noinput
python manage.py check --deploy --fail-level WARNING
python manage.py migrate
