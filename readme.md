you can check project at http://34.80.218.234:8000

HOW TO RUN PROJECT:

create postgresql database named - marketplace with owner - lalavitohack and password - 1

create .env file 
env template:

SECRET_KEY = django-insecure-tl175(qolyr8gw@m=83172nz&5p#$+o4$s-8yni=(3=__z#+fg
EMAIL_HOST_USER = 'enter your data'
EMAIL_HOST_PASSWORD = 'enter your data'
EMAIL_PORT = 587
EMAIL_HOST = smtp.gmail.com
EMAIL_BACKEND = django.core.mail.backends.smtp.EmailBackend
EMAIL_USE_TLS = True
HOST = 'your data or 34.80.218.234:8000'


1. python3 -m venv venv
2. . venv/bin/activate
3. pip install -r req.txt
4. python manage.py runsever
