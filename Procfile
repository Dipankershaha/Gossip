release: python manage.py migrate
web: daphne My_Social_Project.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=My_Social_Project.settings -v2