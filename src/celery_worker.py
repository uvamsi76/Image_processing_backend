from celery import Celery
import time
import pandas as pd
# Initialize Celery
celery_app = Celery(
    "tasks",
    broker_url="redis://localhost:6379/0",  # Redis as the message broker
    result_backend="redis://localhost:6379/0",  # Redis as the result backend
)


@celery_app.task
def add_numbers(a: int, b: int):
    time.sleep(20)
    return a + b

@celery_app.task
def process_image(df):
    df=pd.read_json(df)
    for row in df.iterrows():
        time.sleep(20)
    # db operation to change the image url 
    return 'processed'
