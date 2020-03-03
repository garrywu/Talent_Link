"""Talent_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite.views import *
from django.views.generic import TemplateView  # add

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('test/', index),
    path('myTalent/api/deleteTalent', deleteTalent),
    path('myTalent/api/allTalent', allTalent),
    path('myTalent/api/updTalent', updTalent),
    path('myTalent/api/updData', updData),
    path('talentPool/api', talentPool),
    path('', TemplateView.as_view(template_name='index.html')),  # add\
    path('talentPool/api/upd_favor', updFavor),
    path('myFavor/api/active', favorActive),
    path('myFavor/api/inactive', favorInactive),
    path('myFavor/api/removeFavor', removeFavor),
    path('myFavor/api/restoreFavor', restoreFavor),
    path('myFavor/api/removeFavorall', removeFavorall),
    path('myFavor/api/emptyFavorall', emptyFavorall),
    path('myFavor/api/admireTalent', admireTalent),
    path('uploadTalent/api', uploadTalent),
    path('downloadDoc/api', downloadDoc),


]
