# Django-eLearning-Platform
CM3035 Final Project. Runs on Django

# To enter venv:

>>> source venv/Scripts/activate

# To run Docker:

>>> docker run --name redis -p 6379:6379 -d redis:latest

# To run celery:

>>> celery -A elearning worker -l info --pool=solo

# To run server:

>>> python manage.py runserver

# Admin access:

>>> username : admin
>>> password: admin123
>>> email: admin@courpera.ca