from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from celery import Celery
    from celery.result import AsyncResult
    from sqlalchemy.orm import Session

from my_celery_app import tasks  # noqa


def test_tasks_are_there(celery_app: "Celery"):
    # 10 default tasks, plus 2 from myapp
    assert len(celery_app.tasks) == 14


def test_add_task_add(celery_app: "Celery", celery_worker):
    task: "AsyncResult" = celery_app.tasks["my_celery_app.tasks.regular_tasks.my_super_task"].apply_async(
        (1, 2)
    )
    assert task.state == "PENDING"
    assert task.get() == 3
    assert task.state == "SUCCESS"


def test_add_task_db_check(celery_app: "Celery", celery_worker, task_model):
    from celery.backends.database import DatabaseBackend

    backend = celery_app.backend
    assert isinstance(backend, DatabaseBackend)
    session: "Session" = backend.ResultSession()
    task: "AsyncResult" = celery_app.tasks["my_celery_app.tasks.regular_tasks.my_super_task"].apply_async(
        (1, 2)
    )
    assert task.get() == 3

    with session.begin():
        assert session.query(task_model).count() == 2
        db_result = session.query(task_model).filter_by(task_id=task.id).one()
        assert db_result.result == 3
        assert db_result.status == "SUCCESS"
        assert db_result.name == "my_celery_app.tasks.regular_tasks.my_super_task"
