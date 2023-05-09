from celery.utils.log import get_task_logger

from my_celery_app.celery_app import binded_celery_app
import random

logget = get_task_logger(__name__)


@binded_celery_app.task
def my_super_task(x, y):
    """A debug/sample task that prints the value after {wait} seconds. 
    The task name is 'my_celery_app.tasks.regular_tasks.my_super_task'
    """
    return x + y


@binded_celery_app.task(bind=True)
def long_running_task(self) -> float:
    """A debug/sample task that prints the value after {wait} seconds. 
    The task name is 'my_celery_app.tasks.regular_tasks.long_running_task'
    """
    n = 100000
    total = 0
    for i in range(0, n):
        total += random.randint(1, 1000)
    return total / n
