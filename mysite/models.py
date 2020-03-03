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


class MyTalent(Document):
    _id = ObjectIdField(required=False)
    p_owner = StringField(required=True)
    p_desc = StringField(required=True)
    p_end_dt = StringField(required=True)
    p_name = StringField(required=True)
    p_overview = StringField(required=True)
    p_owner_site = StringField(required=True)
    p_tag = ListField(required=False)
    p_userid = StringField(required=True)
    p_follower = ListField(required=False)
    p_admire = ListField(required=False)
    p_inactive = ListField(required=False)
    p_doc_a = FileField(required=False)
    p_doc_b = FileField(required=False)
    p_doc_c = FileField(required=False)
    p_files_name = ListField(required=False)