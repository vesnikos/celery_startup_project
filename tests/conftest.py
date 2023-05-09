import pytest
from celery import Celery
from pytest_postgresql import factories as pg_factories

broker = "amqp://guest:guest@localhost//"

def prep_database(host, port, user, password, dbname):
    temp_celery_app = Celery(
        "tasks",
        broker=broker,
        backend=f"db+postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}",
    )

    # call so it will trigger the creation of the tables in the temp database
    temp_celery_app.backend.ResultSession()


postgresql_docker = pg_factories.postgresql_noproc(load=[prep_database])
postgresql = pg_factories.postgresql("postgresql_docker")


@pytest.fixture(scope='session')
def celery_parameters():
    from my_celery_app.celery_app import task_routes
    return {
        'broker': broker,
        'task_cls':  'my_celery_app.task_manager.KustomTask',
        'strict_typing': True,
    }

@pytest.fixture(scope="session")
def celery_config(postgresql_docker):
    from my_celery_app.celery_app import task_routes
    return {
        "result_extended": True,
        'task_routes': task_routes,
        "result_backend": "db+postgresql+psycopg://postgres:postgres@localhost:5432/celery-test",
        "broker_url": "memory://",
    }


@pytest.fixture
def celery_app(request, celery_app, postgresql):
    celery_app.conf.update(result_extended=True)
    assert len(celery_app.tasks) == 14
    yield celery_app


@pytest.fixture
def task_model():
    from celery.backends.database import models

    return models.TaskExtended


@pytest.fixture(scope="session")
def celery_worker_parameters():
    return {
        "queues": ("regular_tasks", "debug", "celery"),
    }