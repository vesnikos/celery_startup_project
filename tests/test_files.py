from tasks import *


def test_task(celery_app, celery_worker):
    task = long_running_task.s()
    job = task.apply_async()
    result = job.get()
    print(result)




