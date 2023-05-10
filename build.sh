set -o errexit

pip install -r requirements/production.txt

mkdir /opt/render/project/src/feesprefect/static

python manage.py collectstatic --no-input
python manage.py migrate --run-syncdb
python manage.py shell -c "from django.contrib.contenttypes.models import ContentType; ContentType.objects.all().delete()"
python manage.py loaddata data.json
