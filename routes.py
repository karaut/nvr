from fastapi import FastAPI
from mongoengine import connect
from models import nvr_collection,brand_name_collection
from serializers import nvr_data_body
import json
from passlib.context import CryptContext
from alert_check import nvr
import mapping
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connect(db="nvr_database",host="localhost",port= 27017)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/get_nvr_info")
def get_nvr_info():
    nvr = json.loads(nvr_collection.objects().to_json())
    return {"nvr_info": nvr}


@app.post("/add_nvr_info")
def add_nvr_info(nvr_data: nvr_data_body):
    pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    nvr = nvr_collection(ip = nvr_data.ip,
                        port =nvr_data.port,
                        username = nvr_data.username,
                        password = pwd_context.hash(nvr_data.password),
                        brand_name = nvr_data.brand_name,
                        model_name = nvr_data.model_name)
    nvr.save()
    
    return {"message":"data added successfuly"}

@app.get("/set_brand_name")
def set_brand_name():
    brand_name = []
    nvr = json.loads(brand_name_collection.objects().to_json())
    for i in nvr:
        brand_name.append(i["brand_name"])
    return {"brand_names": brand_name}

@app.post("/get_model_names")
def get_brand_name(brand_name:str):
    nvr = brand_name_collection.objects().get(brand_name = brand_name)
    return {"model_names": nvr.model_name}

@app.get("/search_brand")
def search_brand(brand_name):
    nvr = json.loads(brand_name_collection.objects().filter(brand_name__icontains = brand_name).to_json())
    return{"nvr":nvr}

@app.post("/check_date_time")
def check_date_time():
    n1 = nvr("192.168.1.108","80","admin","admin123")
    responce = n1.check_date_time()
    return{"responce": responce}

@app.post("/check_storage_exist")
def check_storage_exist():
    n1 = nvr("192.168.1.108","80","admin","admin123")
    responce = n1.check_storage_exist()
    return{"responce": responce}

@app.post("/test")
def test():
    val = mapping.mp["daua"]
    final_val = val("192.168.1.108","80","admin","admin123")
    output = final_val.check_storage_exist()
    return{"responce": output}