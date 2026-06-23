## import time
import subprocess
import re
from celery import Celery
from app.config import settings

celery_app=Celery(
    "media_worker",
    broker=settings.REDIS_URL, #where to listen for incoming job
    backend=settings.REDIS_URL #where to save results
)

@celery_app.task(bind=True)#celery library,A wrapper that intercepts your function and turns its parameters into an asynchronous message packet.
def meida_task_converter(self,input_path:str,output_path:str):
    print(f"starting real ffmpeg conversion for: {input_path}")
    self.update_state(state='PROGRESS',meta={'percent':"processing...."})
    # 2. Build our system token list
    ffmpeg_command=[
        "ffprobe",
        "-v","error","-select_streams","v:0",
        "-count_packets","-show_entries","stream=nb_read_packets",
        "-of","csv=p=0",input_path
        
    ]
    try:
        total_frames=int(subprocess.check_output(ffprobe_cmd).decode().strip())
        print(f"totale frames to process: {total_frames}")
    except Exception:
        #fallback default if ffprobe fails to parse a wired file
        total_frames=1000
    #build our real conversion command
    ffmpeg_command=[
        "ffmpeg","-y","-i",input_path,"-progress","pipe:1",output_path
    ]
    #launch the process asynchronously , supprocess.popen is built-in python
    process=subprocess.Popen(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    #4. read the live stdout data pipe lin by line *while* FFmpeg works
    while True:
        line=process.stdout.readline()
        if not line and process.poll() is not None:
            break #exit loop if ffmpeg has completed finished
        if "frame=" in line:
            #extract raw integer number following "frames=" using Regex
            match=re.search(r"frame=\s*(\d+)",line) #re.search is inbuilt python,like textscanner to find specific characters
            if match:
                current_frame=int(match.group(1))
                #math equation
                percent=int((current_frame/total_frames)*100)
                percent=min(percent,99)

                #update our redis scoreboard
                self.update_state(state="PROGRESS",meta={'percent':percent})
                print(f"live project progress:{percent}%")
    
    #double check that progress exited cleanly
    return_code=process.poll()
    if return_code != 0:
        raise RuntimeError(f"FFmpeg failed with exit code{return_code}")

    print(f"conversion completely finished! saved to : {output_path}")
    return {"status":"SUCCESS","output_file":output_path}    

















    # # for i in range(1,6):
    # #     time.sleep(2)
    # #     percent=i*20
    # try:
    #     # 3. Run the compiled FFmpeg system process safely from Python
    #     result=subprocess.run(
    #         ffmpeg_command,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         text=True,
    #         check=True# Automatically throws an exception if FFmpeg returns a non-zero crash exit code
    #     )
    #     print(f"conversion finished successfully, saved to{output_path}")
    #     return{"message":"success","output_file":output_path}
    # except subprocess.CalledProcessError as e:
    #     # 4. If FFmpeg crashes (corrupt file, wrong parameters), capture the error log
    #     print(f"the ffmpeg process crashed,details:{e.stderr}")
    #     raise RuntimeError(f"ffmpeg processing failed:{e.stderr}")
