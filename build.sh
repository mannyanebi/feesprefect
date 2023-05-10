set -o errexit

pip install -r requirements/production.txt

mkdir /opt/render/project/src/feesprefect/static

python manage.py collectstatic --no-input
python manage.py migrate
