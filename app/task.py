import time
from celery import Celery
from app.config import settings

celery_app=Celery(
    "media_worker",
    broker=settings.REDIS_URL, #where to listen for incoming job
    backend=settings.REDIS_URL #where to save results
)

@celery_app.task(bind=True)
def meida_task_converter(self,input_path:str,output_path:str):
    print(f"starting conversion for: {input_path}")

    for i in range(1,6):
        time.sleep(2)
        percent=i*20
    
    self.update_state(state='PROGRESS',meta={'percent':percent})#shares our percentage progress
    print(f"the status is : {percent}%")

    print(f"conversion finished! saved to {output_path}")
    return{"status":"SUCCESS","output path":output_path}