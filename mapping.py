from alert_check import nvr
from models import add_nvr_manualy_info
import json

def get_nvr(ip,port,user_name,password):
    return nvr(ip,port,user_name,password)

mp = {"marol nvr":get_nvr}

def get_dict():
    super_data_list = {}
    data_dict = {}
    auth = json.loads(add_nvr_manualy_info.objects().to_json())
    for i in auth:
        super_data_list[i["nvr_name"]] = {}
        data_dict["nvr_name"] = i["nvr_name"]
        data_dict["nvr_brand_name"] = i["nvr_brand_name"]
        data_dict["nvr_model_name"] = i["nvr_model_name"]
        data_dict["nvr_ip"] = i["nvr_ip"]
        data_dict["nvr_port"] = i["nvr_port"]
        data_dict["nvr_user_name"] = i["nvr_user_name"]
        data_dict["nvr_password"] = i["nvr_password"]
    
    return data_dict

def get_demo():
    super_data_list = {}
    auth = json.loads(add_nvr_manualy_info.objects().to_json())
    for i in auth:
        data_dict = {}
        data_dict["nvr_name"] = i["nvr_name"]
        data_dict["nvr_brand_name"] = i["nvr_brand_name"]
        data_dict["nvr_model_name"] = i["nvr_model_name"]
        data_dict["nvr_ip"] = i["nvr_ip"]
        data_dict["nvr_port"] = i["nvr_port"]
        data_dict["nvr_user_name"] = i["nvr_user_name"]
        data_dict["nvr_password"] = i["nvr_password"]
        super_data_list[i["nvr_name"]] = data_dict

    return super_data_list

