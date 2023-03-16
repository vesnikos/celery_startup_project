import pytest
from celery import Celery
from pytest_postgresql import factories as pg_factories


def prep_database(host, port, user, password, dbname):
    temp_celery_app = Celery(
        "tasks",
        broker="memory://",
        backend=f"db+postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}",
    )

    # call it once to trigger the creation of the tables in the tplt database
    temp_celery_app.backend.ResultSession()


postgresql_docker = pg_factories.postgresql_noproc(load=[prep_database])
postgresql = pg_factories.postgresql("postgresql_docker")


@pytest.fixture(scope="session")
def celery_config(postgresql_docker):
    return {
        "result_extended": True,
        "result_backend": "db+postgresql+psycopg://postgres:postgres@localhost:5432/celery-test",
        "broker_url": "memory://",
    }


@pytest.fixture
def celery_app(request, celery_app, postgresql):
    celery_app.conf.update(result_extended=True)
    assert len(celery_app.tasks) == 12
    yield celery_app


@pytest.fixture
def task_model():
    from celery.backends.database import models

    return models.TaskExtended
