from celery import Celery
from celery.schedules import crontab

app = Celery('server', broker='redis://localhost:6379/0')
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.test',
        'schedule': 5.0,
        'args': ('hello')
    },
}
app.conf.timezone = 'UTC'


@app.task
def test(arg):
    print(arg)