##  How to run locally
    * use .env_example or env_local as reference for creating .env file
1. Run rabbitmq locally
    * inastall rabbitmq package
    * start and/or enable rabbitmq.service
2. Run Django
    * python manage.py runserver
3. Run Celery:
    * celery -A youtube_downloader worker --loglevel=inf

##  How to run on Heroku
    * Open https://youtube-downloader2.herokuapp.com/


##  Notes:
    * There is custom manage.py command 'clear_statistcs', use it for clear the
    daily downloads in the database, which will allow new downloads for the new
    day
