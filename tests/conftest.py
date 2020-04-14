import pytest
from pathlib import Path
from worker import capp
import celery.contrib.testing.tasks


@pytest.fixture(scope='session')
def celery_config(tmpdir_factory):
    tmpdir = Path(tmpdir_factory.getbasetemp())

    broker_folder = tmpdir / '__broker'
    out = broker_folder / 'out'
    processed = broker_folder / 'processed'

    if not broker_folder.is_dir():
        broker_folder.mkdir()
        out.mkdir()
        processed.mkdir()
    return {

        'broker_url': 'filesystem://',
        'broker_transport_options': {
            'data_folder_in': f'{out.as_posix()}',
            'data_folder_out': f'{out.as_posix()}',
            'data_folder_processed': f'{processed.as_posix()}'
        },

        'result_persistent': False,
        'task_serializer': 'json',
        'result_serializer': 'json',
        'accept_content': ['json'],
        'result_backend': 'cache',
        'cache_backend': 'memory'
    }


@pytest.fixture(scope='session')
def celery_enable_logging():
    return True


@pytest.fixture(scope='session')
def celery_includes():
    return [
        'celery.contrib.testing.tasks'
    ]


@pytest.fixture(scope='session')
def celery_worker_pool():
    return 'solo'


@pytest.fixture(scope='session')
def celery_app(request,
               celery_config,
               celery_parameters,
               celery_enable_logging,
               use_celery_app_trap):

    capp.conf.update(celery_config)
    return capp
