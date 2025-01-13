import time
from app import celery, get_redis_instance, create_celery_app

if not celery:
    celery = create_celery_app()
redis_client = get_redis_instance()


@celery.task(bind=True)
def long_running_task(self, duration):
    """Simulate a long-running task."""
    task_id = self.request.id

    redis_client.hset(f"task:{task_id}", "status", "PROCESSING")

    try:
        time.sleep(duration)

        redis_client.hset(f"task:{task_id}", "status", "COMPLETED")
        redis_client.hset(
            f"task:{task_id}", "result", f"Task completed in {duration} seconds"
        )
    except Exception as e:
        redis_client.hset(f"task:{task_id}", "status", "FAILED")
        redis_client.hset(f"task:{task_id}", "result", str(e))
        raise
