import mongoengine as db

class nvr_collection(db.Document):
    ip = db.StringField()
    port = db.IntField()
    username = db.StringField()
    password = db.StringField()
    brand_name = db.StringField()
    model_name = db.ListField()

    # def set_password(self, password):
    #     self.Password = pwd_context.hash(password)

class brand_name_collection(db.Document):
    brand_name = db.StringField()
    model_name = db.ListField()

class add_nvr_manualy_info(db.Document):
    nvr_name = db.StringField()
    nvr_brand_name = db.StringField()
    nvr_model_name = db.StringField()
    nvr_ip = db.StringField()
    nvr_port = db.StringField()
    nvr_user_name = db.StringField()
    nvr_password = db.StringField()
