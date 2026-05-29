# Sabzlearn Django Project

## Quick Setup

# Clone the repository
git clone https://github.com/ErenYeager08/sabzlearn.git
- cd sabzlearn

# Setup virtual environment
python -m venv venv  
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Database setup
python manage.py makemigrations  
python manage.py migrate --settings=core.settings.deployment

# Static files
python manage.py collectstatic

# Run server
python manage.py runserver --settings=core.settings.deployment
