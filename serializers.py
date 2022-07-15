from pydantic import BaseModel
class nvr_data_body(BaseModel):
    ip: str
    port:int
    username:str
    password :str
    brand_name:str
    model_name:list