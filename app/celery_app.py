from celery import Celery

from app import Config

class CeleryConfig:
    task_acks_late = True
    task_reject_on_worker_lost = True

def create_celery_app(app=None):
    """Create a standalone Celery app."""
    celery = Celery(
        "tasks",
        backend=Config.CELERY_RESULT_BACKEND,
        broker=Config.CELERY_BROKER_URL,
    )

    celery.config_from_object(CeleryConfig)
    if app:

        TaskBase = celery.Task

        class ContextTask(TaskBase):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)

        celery.Task = ContextTask

    return celery
