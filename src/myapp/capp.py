from celery import Celery

capp = Celery("tasks", broker="amqp://guest@localhost//")
capp.autodiscover_tasks(force=True)
