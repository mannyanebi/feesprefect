set -o errexit

pip install -r requirements/production.txt

python manage.py migrate
