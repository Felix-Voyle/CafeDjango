set -o errexit

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Make migrations and migrate database
python manage.py makemigrations
python manage.py migrate

# Create superuser if not exists
python manage.py createsuperuser --no-input