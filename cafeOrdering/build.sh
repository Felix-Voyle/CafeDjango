set -o errexit

# Check if pip and python commands exist
if ! command -v pip &> /dev/null || ! command -v python &> /dev/null; then
    echo "Error: Python or pip commands not found. Please ensure Python is installed."
    exit 1
fi

# Activate virtual environment if applicable
# Replace '/path/to/venv/bin/activate' with the path to your virtual environment activation script
source cafeOrdering/venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Make migrations and migrate database
python manage.py makemigrations
python manage.py migrate

# Create superuser if not exists
python manage.py createsuperuser --no-input