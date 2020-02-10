from mongoengine import *
import datetime


class InfoTest(Document):
    title = StringField(required=True)
    address = StringField(required=True)
    flood = StringField(required=True)
    followInfo = StringField(required=True)
    img_url = StringField(required=True)
    image_id = StringField(required=True)
    create_time = DateTimeField(required=True)