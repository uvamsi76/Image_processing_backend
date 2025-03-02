from celery import Celery
import time
import pandas as pd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import requests
from io import BytesIO
from PIL import Image
import pandas as pd
import ast


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

def authenticate_drive():
    """Authenticate and return a Google Drive instance"""
    scope = ["https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
    
    gauth = GoogleAuth()
    gauth.credentials = credentials
    return GoogleDrive(gauth)


def upload_to_drive(filename="compressed.jpg",drive=None):
    if(drive==None):
        drive = authenticate_drive()
    img_file = drive.CreateFile({'title': filename})
    img_file.SetContentFile(filename)
    img_file.Upload()
    
    # Make file public
    img_file.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader'})
    
    return f"https://drive.google.com/uc?id={img_file['id']}"

@celery_app.task
def process_image(df):
    df=pd.read_json(df)
    df['Processed Image Urls']=None
    url = "https://catbox.moe/user/api.php"
    for i,row in df.iterrows():
        a=ast.literal_eval(row['Input Image Urls'])
        # print(a)
        b=[]
        for j,image_url in enumerate(a):
            file_id = image_url.split("id=")[1]
            response = requests.get(image_url)
            if response.status_code != 200:
                print('issue with getting image')
            img = Image.open(BytesIO(response.content))
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            output_filename = f'compressed-{file_id}'
            img.save(f'src/compressed/compressed-{file_id}.jpg', format="JPEG", quality=50)
            files = {"fileToUpload": open(f"src/compressed/compressed-{file_id}.jpg", "rb")}
            data = {"reqtype": "fileupload"}
            response = requests.post(url, files=files, data=data)
            drive_link=response.text
            b.append(drive_link)
        df.loc[i, 'Processed Image Urls'] = str(b)
    print(df.head())
    # db operation to change the image url
    
    return df.to_dict()
