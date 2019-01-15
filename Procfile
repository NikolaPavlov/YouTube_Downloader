web: gunicorn youtube_downloader.wsgi --log-file -
worker: celery -A youtube_downloader worker --loglevel=info
