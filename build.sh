set -o errexit

pip install -r requirements/production.txt

mkdir static

python manage.py collectstatic --no-input
python manage.py migrate
