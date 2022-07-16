from fastapi import FastAPI
from mongoengine import connect
from models import brand_name_collection,add_nvr_manualy_info
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

@app.post("/addnvrinfo")
def add_nvr_info(nvr_data: nvr_data_body):
    pwd_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
    nvr = add_nvr_manualy_info(nvr_name = nvr_data.nvr_name,
                        nvr_brand_name = nvr_data.nvr_brand_name,
                        nvr_model_name = nvr_data.nvr_model_name,
                        nvr_ip = nvr_data.nvr_ip,
                        nvr_port = nvr_data.nvr_port,
                        nvr_user_name = nvr_data.nvr_user_name,
                        nvr_password = nvr_data.nvr_password
                        )
    nvr.save()
    return {"message":"data added successfuly"}

@app.get("/nvrinfo")
def read_nvr_info():
    data_dict = mapping.get_dict()
    return data_dict

@app.post("/autocorrectdate")
def check_date_time():
    data_dict = mapping.get_dict()
    nvr_name = mapping.mp[data_dict["nvr_name"]]
    nvr_obj = nvr_name(data_dict["nvr_ip"],data_dict["nvr_port"],data_dict["nvr_user_name"],data_dict["nvr_password"])
    responce = nvr_obj.check_date_time()
    return{"responce": responce,"data_dict":data_dict}

@app.post("/check_storage_exist")
def check_storage_exist():
    data_dict = mapping.get_dict()
    nvr_name = mapping.mp[data_dict["nvr_name"]]
    nvr_obj = nvr_name(data_dict["nvr_ip"],data_dict["nvr_port"],data_dict["nvr_user_name"],data_dict["nvr_password"])
    responce = nvr_obj.check_storage_exist()
    return{"responce": responce}

@app.post("/check_storage_accessable")
def check_storage_accessable():
    data_dict = mapping.get_dict()
    nvr_name = mapping.mp[data_dict["nvr_name"]]
    nvr_obj = nvr_name(data_dict["nvr_ip"],data_dict["nvr_port"],data_dict["nvr_user_name"],data_dict["nvr_password"])
    responce = nvr_obj.check_storage_accessable()
    return{"responce": responce}

@app.get("/get_brand_name")
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

@app.get("/test")
def test():
    data_dict = mapping.get_demo()
    return data_dict["marol nvr"]["nvr_brand_name"]


