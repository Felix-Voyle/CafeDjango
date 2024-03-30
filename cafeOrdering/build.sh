set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files
echo "yes" | python manage.py collectstatic

# Make migrations and migrate database
python manage.py makemigrations
python manage.py migrate --run-syncdb


#echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'felix.voyle@icloud.com', 'run12345')" | python manage.py shell
