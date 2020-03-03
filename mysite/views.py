from django.http import HttpResponse
from django.shortcuts import render
from mysite.models import InfoTest
from mysite.models import MyTalent
from django.views.decorators.csrf import csrf_exempt
from bson.objectid import ObjectId
from bson import json_util
from django.http import StreamingHttpResponse
from django.http import FileResponse
import binascii
import os
import tempfile
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg
import json
import time
import logging
import pymongo
import gridfs

#use pymongo for file delete and update
client = pymongo.MongoClient("localhost", 27017)
db = client.talent

# 生成一个以当前文件名为名字的logger实例
logger = logging.getLogger(__name__)


def index(request):
    demo = InfoTest(title='test2',
                    address='test2',
                    flood='test1',
                    followInfo='test1',
                    img_url='https://baidu.com',
                    image_id='5b344a2bf5d127b854216556',
                    create_time=time.strftime('%Y-%m-%d %H:%M:%S'))
    demo.save()
    return render(request, "index.html")


@csrf_exempt
def allTalent(request):
    b_mylist = MyTalent.objects.filter(p_userid="1")
    mylist = json_util.dumps(b_mylist._collection_obj.find(b_mylist._query))
    print(mylist)
    logger.debug("一个萌萌的请求过来了。。。。")
    logger.info("一个更萌的请求过来了。。。。")
    return HttpResponse(mylist, content_type="application/json")

@csrf_exempt
def talentPool(request):
    b_totallist = MyTalent.objects.all()
    totallist = json_util.dumps(b_totallist._collection_obj.find(b_totallist._query))
    return HttpResponse(totallist, content_type="application/json")

@csrf_exempt
def updFavor(request):
    if request.method == 'POST':
        message = "updated"
        upd_id = request.POST.get("upd_id", None)
        upd_favor = request.POST.get("upd_favor", None)
        upd_arr = upd_favor.split(',')
        print(upd_arr)
        # 根据条件修改数据
        cur_res = MyTalent.objects.filter(_id = upd_id)
        cur_res_json = json_util.dumps(cur_res._collection_obj.find(cur_res._query))

        cur_res_json_text = json.loads(cur_res_json)
        cur_follower = cur_res_json_text[0].get("p_follower")

        if upd_favor not in cur_follower:
            cur_follower.append(upd_favor)
        result = MyTalent.objects.filter(_id = upd_id).update(p_follower = cur_follower )

    return HttpResponse(message)

@csrf_exempt
def favorActive(request):
    if request.method == 'POST':
        user_id = request.POST.get("user_id", None)
        # 根据条件修改数据
        cur_alist = MyTalent.objects(p_follower = user_id)
        active_list = json_util.dumps(cur_alist._collection_obj.find(cur_alist._query))
        print(active_list)
        return HttpResponse(active_list, content_type="application/json")

@csrf_exempt
def favorInactive(request):
    if request.method == 'POST':
        in_user_id = request.POST.get("user_id", None)
        # 根据条件修改数据
        cur_inalist = MyTalent.objects(p_inactive = in_user_id)
        inactive_list = json_util.dumps(cur_inalist._collection_obj.find(cur_inalist._query))
        return HttpResponse(inactive_list, content_type="application/json")

@csrf_exempt
def removeFavor(request):
    if request.method == 'POST':
        message = "updated"
        remove_id = request.POST.get("remove_id", None)
        remove_user = request.POST.get("remove_user", None)
        # 根据条件修改数据
        cur_removelist = MyTalent.objects.filter(_id = remove_id)

        cur_removelist_json = json_util.dumps(cur_removelist._collection_obj.find(cur_removelist._query))

        cur_remove_json_text = json.loads(cur_removelist_json)
        cur_follower = cur_remove_json_text[0].get("p_follower")
        cur_inactive = cur_remove_json_text[0].get("p_inactive")

        if remove_user in cur_follower:
            cur_follower.remove(remove_user)
            if remove_user not in cur_inactive:
                cur_inactive.append(remove_user)

        result = MyTalent.objects.filter(_id=remove_id).update(p_follower=cur_follower, p_inactive=cur_inactive)

        return HttpResponse(message)

@csrf_exempt
def removeFavorall(request):
    if request.method == 'POST':
        message = "updated"
        remove_id = []
        remove_id = request.POST.get("remove_id", None)
        remove_id = remove_id.split(",")
        remove_user = request.POST.get("remove_user", None)

        for i in remove_id:
            if ObjectId.is_valid(i):
                o_id = ObjectId(i)
            cur_removeall_list = MyTalent.objects.filter(_id=o_id)

            cur_removeall_list_json = json_util.dumps(cur_removeall_list._collection_obj.find(cur_removeall_list._query))

            cur_removeall_json_text = json.loads(cur_removeall_list_json)
            cur_remove_follower = cur_removeall_json_text[0].get("p_follower")
            cur_remove_inactive = cur_removeall_json_text[0].get("p_inactive")

            if remove_user in cur_remove_follower:
                cur_remove_follower.remove(remove_user)
                if remove_user not in cur_remove_inactive:
                    cur_remove_inactive.append(remove_user)

            result = MyTalent.objects.filter(_id=o_id).update(p_follower=cur_remove_follower,
                                                                   p_inactive=cur_remove_inactive)
        return HttpResponse(message)

@csrf_exempt
def restoreFavor(request):
    if request.method == 'POST':
        message = "updated"
        restore_id = request.POST.get("restore_id", None)
        restore_user = request.POST.get("restore_user", None)
        # 根据条件修改数据
        cur_restorelist = MyTalent.objects.filter(_id = restore_id)

        cur_restorelist_json = json_util.dumps(cur_restorelist._collection_obj.find(cur_restorelist._query))

        cur_restore_json_text = json.loads(cur_restorelist_json)
        cur_follower = cur_restore_json_text[0].get("p_follower")
        cur_inactive = cur_restore_json_text[0].get("p_inactive")

        if restore_user in cur_inactive:
            cur_inactive.remove(restore_user)
            if restore_user not in cur_follower:
                cur_follower.append(restore_user)

        result = MyTalent.objects.filter(_id=restore_id).update(p_follower=cur_follower, p_inactive=cur_inactive)

        return HttpResponse(message)

@csrf_exempt
def emptyFavorall(request):
    if request.method == 'POST':
        message = "updated"
        empty_id = []
        empty_id = request.POST.get("empty_id", None)
        empty_id = empty_id.split(",")
        empty_user = request.POST.get("empty_user", None)

        for i in empty_id:
            if ObjectId.is_valid(i):
                o_id = ObjectId(i)
            cur_emptyall_list = MyTalent.objects.filter(_id=o_id)

            cur_emptyall_list_json = json_util.dumps(
                cur_emptyall_list._collection_obj.find(cur_emptyall_list._query))

            cur_emptyall_json_text = json.loads(cur_emptyall_list_json)
            cur_emptyall_inactive = cur_emptyall_json_text[0].get("p_inactive")

            if empty_user in cur_emptyall_inactive:
                cur_emptyall_inactive.remove(empty_user)

            result = MyTalent.objects.filter(_id=o_id).update(p_inactive=cur_emptyall_inactive)

        return HttpResponse(message)

@csrf_exempt
def admireTalent(request):
    if request.method == 'POST':
        message = "updated"
        admire_id = request.POST.get("admire_id", None)
        admire_user = request.POST.get("admire_user", None)
        # 根据条件修改数据
        cur_admirelist = MyTalent.objects.filter(_id = admire_id)

        cur_admirelist_json = json_util.dumps(cur_admirelist._collection_obj.find(cur_admirelist._query))

        cur_admire_json_text = json.loads(cur_admirelist_json)
        cur_admire = cur_admire_json_text[0].get("p_admire")

        if admire_user not in cur_admire:
            cur_admire.append(admire_user)
        else:
            message = 'failed'

        result = MyTalent.objects.filter(_id=admire_id).update(p_admire=cur_admire)

        return HttpResponse(message)

@csrf_exempt
def uploadTalent(request):
    if request.method == 'POST':
        message = "uploaded"
        file_path = ""

        p_owner = request.POST.get("p_owner", None)
        p_desc = request.POST.get("p_desc", None)
        p_owner_site = request.POST.get("p_owner_site", None)
        p_end_dt = request.POST.get("p_end_dt", None)
        p_name = request.POST.get("p_name", None)
        p_overview = request.POST.get("p_overview", None)
        p_tag_ori = request.POST.get("p_tag", None)
        p_userid = request.POST.get("p_userid", None)
        p_tag = p_tag_ori.split(",")
        p_file_list = request.FILES.getlist("file", None)

        upd_talent = MyTalent()
        upd_talent.p_owner = p_owner
        upd_talent.p_desc = p_desc
        upd_talent.p_end_dt = p_end_dt
        upd_talent.p_name = p_name
        upd_talent.p_overview = p_overview
        upd_talent.p_userid = p_userid
        upd_talent.p_tag = p_tag
        upd_talent.p_follower = []
        upd_talent.p_owner_site = p_owner_site
        upd_talent.p_admire = []
        upd_talent.p_inactive = []

        pwd = os.getcwd()
        file_length = len(p_file_list);
        p_files_name = [];

        if file_length > 0:
            # upd_talent.p_doc_a.new_file()
            fa = p_file_list[0].name
            p_files_name.append(fa)
            file_path = os.path.join(pwd, 'upload', fa + upd_talent.p_userid)
            f = open(file_path, mode="wb")
            for i in p_file_list[0].chunks():
                f.write(i)
            f.close()
            file_bytes = open(file_path, "rb")
            upd_talent.p_doc_a.put(file_bytes, content_type=p_file_list[0].content_type, filename=p_file_list[0].name)
            # for chunk in p_file_list[0].chunks():
            #     upd_talent.p_doc_a.write(chunk)
            # upd_talent.p_doc_a.close()
            # upd_talent.p_doc_a.put(content_type=p_file_list[0].content_type, filename=p_file_list[0].name)

        if file_length > 1:
            # upd_talent.p_doc_b.new_file()
            fb = p_file_list[1].name
            p_files_name.append(fb)
            file_path = os.path.join(pwd, 'upload', fb + upd_talent.p_userid)
            f = open(file_path, mode="wb")
            for i in p_file_list[1].chunks():
                f.write(i)
            f.close()
            file_bytes = open(file_path, "rb")
            upd_talent.p_doc_b.put(file_bytes, content_type=p_file_list[1].content_type, filename=p_file_list[1].name)

        if file_length == 3:
            upd_talent.p_doc_c.new_file()
            fc = p_file_list[2].name
            p_files_name.append(fc)
            file_path = os.path.join(pwd, 'upload', fc + upd_talent.p_userid)
            f = open(file_path, mode="wb")
            for i in p_file_list[2].chunks():
                f.write(i)
            f.close()
            file_bytes = open(file_path, "rb")
            upd_talent.p_doc_c.put(file_bytes, content_type=p_file_list[2].content_type, filename=p_file_list[2].name)

        upd_talent.p_files_name = p_files_name

        upd_talent.save()
        # result = MyTalent.objects.create(p_owner=p_owner, p_desc=p_desc, p_end_dt=p_end_dt, p_name=p_name,
        #                                  p_overview=p_overview, p_userid=p_userid, p_tag=p_tag, p_follower=p_follower,
        #                                  p_owner_site=p_owner_site, p_admire=p_admire, p_inactive=p_inactive)

        return HttpResponse(message)

@csrf_exempt
def deleteTalent(request):
    if request.method == 'POST':
        message = "deleted"
        delete_id = request.POST.get("delete_id", None)
        delete_user = request.POST.get("delete_user", None)
        # 根据条件修改数据

        my_talent = MyTalent.objects.filter(_id = delete_id, p_userid = delete_user)
        my_talent_json = json_util.dumps(my_talent._collection_obj.find(my_talent._query))

        cur_del_json_text = json.loads(my_talent_json)
        doc_a_id = cur_del_json_text[0].get("p_doc_a")
        doc_b_id = cur_del_json_text[0].get("p_doc_b")
        doc_c_id = cur_del_json_text[0].get("p_doc_c")

        if doc_a_id:
            t_doc_a_id = doc_a_id.get('$oid')
            fs = gridfs.GridFS(db)
            fs.delete(ObjectId(t_doc_a_id))

        if doc_b_id:
            t_doc_b_id = doc_b_id.get('$oid')
            fs = gridfs.GridFS(db)
            fs.delete(ObjectId(t_doc_b_id))

        if doc_c_id:
            t_doc_c_id = doc_c_id.get('$oid')
            fs = gridfs.GridFS(db)
            fs.delete(ObjectId(t_doc_c_id))

        result = MyTalent.objects.filter(_id = delete_id, p_userid = delete_user).delete()
        print(message)
        return HttpResponse(message)

@csrf_exempt
def updTalent(request):
    if request.method == 'POST':
        message = "updated"
        upd_id = request.POST.get("upd_id", None)
        upd_user = request.POST.get("upd_user", None)
        # 根据条件修改数据
        cur_updlist = MyTalent.objects.filter(_id = upd_id, p_userid = upd_user)

        cur_updlist_json = json_util.dumps(cur_updlist._collection_obj.find(cur_updlist._query))

        return HttpResponse(cur_updlist_json, content_type="application/json")

@csrf_exempt
def updData(request):
    if request.method == 'POST':
        message = "uploaded"
        p_upd_oid = request.POST.get("p_oid", None)
        p_upd_owner = request.POST.get("p_owner", None)
        p_upd_desc = request.POST.get("p_desc", None)
        p_upd_owner_site = request.POST.get("p_owner_site", None)
        p_upd_end_dt = request.POST.get("p_end_dt", None)
        p_upd_name = request.POST.get("p_name", None)
        p_upd_overview = request.POST.get("p_overview", None)
        p_upd_tag_ori = request.POST.get("p_tag", None)
        p_upd_userid = request.POST.get("p_userid", None)
        p_upd_tag = p_upd_tag_ori.split(",")
        result = MyTalent.objects.filter(_id=p_upd_oid).update(p_owner=p_upd_owner, p_desc=p_upd_desc, p_end_dt=p_upd_end_dt,
                                                           p_name=p_upd_name,p_overview=p_upd_overview, p_userid=p_upd_userid,
                                                           p_tag=p_upd_tag, p_owner_site=p_upd_owner_site)
        return HttpResponse(message)



@csrf_exempt
def downloadDoc(request):
    if request.method == 'POST':
        message = "uploaded"
        doc_download = ""
        doc_name = ""
        p_type = ""
        p_dl_oid = request.POST.get("objid", None)
        p_dl_seq = request.POST.get("doc_seq", None)
        p_dl_docid = request.POST.get("docid", None)
        if p_dl_seq == '0':
            result = MyTalent.objects(_id=p_dl_oid).first()
         # result = MyTalent.objects(_id=p_dl_oid, p_doc_a=p_dl_docid)
            if result:
                p_test = result.p_doc_a
                p_type = result.p_doc_a.content_type
                doc_name = result.p_doc_a.filename
                doc_download = result.p_doc_a.read()
            else:
                message = "not match"
                return HttpResponse(message)

        if p_dl_seq == '1':
            result = MyTalent.objects(_id=p_dl_oid).first()
            if result:
                doc_name = result.p_doc_b.filename
                p_type = result.p_doc_b.content_type
                doc_download = result.p_doc_b.read()
            else:
                message = "not match"
                return HttpResponse(message)

        if p_dl_seq == '2':
            result = MyTalent.objects(_id=p_dl_oid).first()
            if result:
                doc_name = result.p_doc_c.filename
                p_type = result.p_doc_c.content_type
                doc_download = result.p_doc_c.read()
            else:
                message = "not match"
                return HttpResponse(message)

        fp = tempfile.NamedTemporaryFile(delete=False)

        # fp.close()
        print(fp.name)
        with open(fp.name, "wb") as file:
            file.write(doc_download)
        file_r = open(fp.name, "rb")
        # response = FileResponse(file_r)
        response = FileResponse(file_r)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="'+doc_name+'"'
        # os.remove(fp.name)
        return response



