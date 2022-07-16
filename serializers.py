from pydantic import BaseModel
class nvr_data_body(BaseModel):
    nvr_name: str
    nvr_brand_name:str
    nvr_model_name:str
    nvr_ip:str
    nvr_port:str
    nvr_user_name:str
    nvr_password:str