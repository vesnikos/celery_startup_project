from celery.utils.log import get_task_logger
from random import random
from my_celery_app.celery_app import binded_celery_app


logger = get_task_logger(__name__)

@binded_celery_app.task(bind=True)
def task_debug_wait(self, value, wait=0, verbose=True):
    """A debug/sample task that prints the value after {wait} seconds
    The task name is 'my_celery_app.tasks.debug.task_debug_wait'
    """
    if verbose:
        logger.info("Request: {0!r}".format(self.request))
    if wait > 0:
        import time

        time.sleep(wait)

    return value


@binded_celery_app.task
def task_debug_sometimes_fail(fail_percentage=0.8, verbose=True) -> str:
    """ A debug/sample task that fails sometimes 
    The task name is 'my_celery_app.tasks.debug.task_debug_sometimes_fail'
    """
    if random() > 1 - fail_percentage:
        if verbose:
            logger.info("retrying")
        raise Exception(":)")
    return "Finished"
