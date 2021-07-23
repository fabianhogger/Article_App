"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.news_list,name='news'),
    path('news',views.news_list,name='news'),
    path('scrape',views.train,name='scrape'),
    path('libraries',views.libraries,name='libraries'),
    path('library/<str:id>',views.open_library,name='library'),
    path('create_library',views.create_library,name='create_library'),
    path('add_to_lib/<str:name>/<int:id>',views.add_to_lib,name='add_art_to_lib'),
    path('article/<int:id>/',views.retrieve_article,name='article'),
    path('subm',views.subm,name='subm'),
    path('topics',views.topics,name='topics'),
    path('submition',views.submit,name='submit'),
    path('images',views.images,name='images'),
    path('get_similar',views.get_similar,name='get_similar')

]
