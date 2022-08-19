from typing import List
from fastapi import FastAPI,File,UploadFile,Form,Request
from fastapi.templating import Jinja2Templates
from python_speech_features import mfcc
import scipy.io.wavfile as wav
import numpy as np
from tempfile import TemporaryFile

from core import pred_gen

import math
import numpy as np
from collections import defaultdict
import shutil
app = FastAPI()


templates = Jinja2Templates(directory="templates")
@app.get("/")
def read_root(request:Request):
    context = {'request': request,"genre":""}
    return templates.TemplateResponse("index.html",context=context)


@app.post("/uploadfiles/")
def create_upload_files(request:Request,files: List[UploadFile]):
    file_name = [file.filename for file in files]
    file_location = f"unknown/{file_name[0]}"
    with open(file_location, "wb+") as file_object:

        # shutil.copyfileobj([], file_object) 
        for file in files:   
            file_object.write(file.file.read())
        result = pred_gen(r"{}".format(file_location))    
    #return {"info": f"file '{file_name[0]}' saved at '{file_location}and gnere is {result}'"}
    context = {'request': request,"genre":result}
    return templates.TemplateResponse("index.html",context=context)