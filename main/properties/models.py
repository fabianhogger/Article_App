from django.db import models
from django.utils import timezone
from phone_field import PhoneField
from django.db.models import IntegerField, Model
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
class Property(models.Model):
    name=models.CharField(max_length=100,default="")
    url=models.CharField(max_length=200,default="")
    body=models.CharField(max_length=10000,default="")
    image_file = models.ImageField(max_length=700,upload_to='media', default='default.jpg')
    image_url = models.URLField(max_length=700,default='www.noimage.com')
    #Here we store for each article the ids of the article similar to it
    similar_ids=ArrayField(models.IntegerField(), default=list,blank=True)

    def __str__(self):
        return self.name
"""
the library stores the article ids
"""
class Library(models.Model):
    title=models.CharField(max_length=30,default="new_library")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article_ids=ArrayField(models.IntegerField(), default=list,blank=True)
    def __str__(self):
        return "%s %s" % (self.user,self.title)
