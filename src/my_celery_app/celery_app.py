from celery import Celery



task_routes = {
    'my_celery_app.tasks.regular_tasks.*': {'queue':'regular_tasks'},
    'my_celery_app.tasks.debug.*': {'queue': 'debug'},
}

broker="amqp://guest:guest@localhost//" # default broker

binded_celery_app = Celery("tasks", broker=broker, task_routes=task_routes)
binded_celery_app.autodiscover_tasks(force=True,packages=['my_celery_app.tasks'])
binded_celery_app.conf.task_routes = task_routes # not to be confused with task_queues (see below)

### 
# from kombu import Queue
# task_queues = (
#    Queue('default',    routing_key='my_celery_app.tasks.default.#'),
#    Queue('regular_tasks', routing_key='my_celery_app.tasks.regular_tasks.#'),
#    Queue('debug', routing_key='my_celery_app.tasks.debug.#'),
# )
