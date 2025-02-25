from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from src.celery_worker import add_numbers,celery_app,process_image
from src.utils import is_valid
from celery.result import AsyncResult
import pandas as pd
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "FastAPI with Celery is alive!"}

@app.get("/add/{a}/{b}")
def add_task(a: int, b: int):
    task = add_numbers.delay(a, b)  # Run task asynchronously
    return {"task_id": task.id, "status": "Processing"}


@app.get("/task/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id,app=celery_app)
    return {"task_id": task_id, "result":result.result,"status":result.status}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        df=pd.read_csv(file.file).to_json()
    except Exception as e:
        return JSONResponse(content=e,status_code=400)
    
    if(not is_valid(df)):
        return JSONResponse(content='File does not have the expected template',status_code=400)
    try:
        task=process_image.delay(df)
    except Exception as e:
        return JSONResponse(content=e,status_code=400)
    return JSONResponse(content={"task_id": task.id, "status": "Processing"})