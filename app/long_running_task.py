from app import celery
import time

@celery.task(bind=True)
def long_running_task(self, duration):
    """Simulate a long-running task."""
    time.sleep(duration)
    return f"Task completed in {duration} seconds"