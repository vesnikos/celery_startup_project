from typing import Any, Dict, Tuple
from billiard.einfo import ExceptionInfo
import celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

class KustomTask(celery.Task):
    def before_start(self, task_id: str, args:Tuple[Any, ...], kwargs:Dict[str, Any]):
        print("before_run")
        logger.info("before_run")
    def on_retry(self, exc: Any, task_id: str, args: Tuple[Any, ...], kwargs: Dict[str, Any], einfo: ExceptionInfo) -> None:
        print("on_retry")
    def on_success(self, retval, task_id, args, kwargs):
        logger.info("on_success")
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.info("{0!r} failed: {1!r}".format(task_id, exc))
    def after_return(self, status: Any, retval: Any, task_id: str, args: Tuple[Any, ...], kwargs: Dict[str, Any], einfo: ExceptionInfo) -> None:
        print("after_return")
    
