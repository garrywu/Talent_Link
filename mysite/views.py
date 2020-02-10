from django.shortcuts import render
from mysite.models import InfoTest
import time


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

def search(request):
    result = InfoTest.objects.filter(title='test2')
    addr = result[0].address
    return render(request, 'search.html', {"t_address":addr})