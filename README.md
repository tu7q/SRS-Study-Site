# SRS-Study-Site
Website to study school subjects

scp -r /publish-location/* username@hostname:/home/pi/deployment-location


# remember to clear sessions once per day at midnight using cron jobs
-> Nope not anymore
Instead use celery to schedule things:
start broker (redis): sudo service redis-server start
start celery worker:
    on windows:
        python -m pip install gevent
        celery -A WebApp worker -l INFO -P gevent
    linux distro:
        celery -A WebApp worker -l INFO
start celery beats (scheduler): celery -A WebApp beat
