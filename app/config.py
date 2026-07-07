import os

class Settings:
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Celery Beat Schedule Configuration Dictionary
    CELERY_BEAT_SCHEDULE = {
        "run-janitor-every-10-seconds": {
            "task": "app.tasks.auto_cleanup_janitor_task",
            "schedule": 10.0,  # We set this to 10 seconds so we can see it work instantly!
        }
    }

settings = Settings()