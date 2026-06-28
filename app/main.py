import os
import shutil #We use it specifically to copy file streams directly to your disk.
from fastapi import FastAPI,HTTPException,UploadFile,File,Query
from fastapi.responses import JSONResponse
from app.tasks import celery_app,meida_task_converter

app=FastAPI(title="asynchronous media converter api")

UPLOAD_DIR="data/uploads"
OUTPUT_DIR="data/outputs"
os.makedirs(UPLOAD_DIR,exist_ok=True)
os.makedirs(OUTPUT_DIR,exist_ok=True)

ALLOWED_TARGET_FORMATS={'avi','mp3','gif','mkv'}

@app.post("/api/v1/media/convert")
async def convert_media(file:UploadFile=File(...),target_format:str=Query("avi",description="the target format extension to convert to")): #(...) makes upload mandatory
    if not file.filename.endswith(".mp4"):
        raise HTTPException(status_code=400,detail="only .mp4 files are supported")
    input_path=os.path.join(UPLOAD_DIR,file.filename)
    output_filename=file.filename.rsplit(".",1)[0]+".avi" #splits like ["my_movie", "mp4"]
    output_path=os.path.join(OUTPUT_DIR,output_filename)

    with open(input_path,"wb") as buffer:
        shutil.copyfileobj(file.file,buffer)#streams the raw upload binary data straight from the incoming network 
        #stream (file.file) directly into our newly opened file buffer on the hard drive
    task=meida_task_converter.delay(input_path,output_path) #This tells Celery: "Hey, package up a small text note 
    #containing the input_path and output_path strings, and throw it into the Redis queue."

    return JSONResponse(
        status_code=202,
        content={"message":"file upload successfull","task_id":task.id}
    )

@app.get("/api/v1/media/{task_id}")
async def get_task_status(task_id:str):
    task_result=celery_app.AsyncResult(task_id)
    response_data={"task_id":task_id,"status":task_result.state}
    if task_result.state=="PROGRESS":
        response_data["progress"]=task_result.info.get("percent")
    elif task_result.state=="SUCCESS":
        response_data["progress"]=100
        response_data["result"]=task_result.result
    elif task_result.state=="FAILURE":
        response_data["error"]=str(task_result.info)
    return response_data
