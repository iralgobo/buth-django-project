celery -A config worker -l info --pool=solo

celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
