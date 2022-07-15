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


