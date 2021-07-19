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
    views=models.IntegerField(default=0)
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

class Entity(models.Model):
    """docstring for Entity."""
    name=models.CharField(max_length=128,unique=True)
    class Ent_Type(models.TextChoices):
        PERSON='PERSON'
        GEOPOLITICAL_ENTITY='GPE'
        ORGANIZATION='ORG'
        GEOGRAPHICAL_ENTITY='GEO'
    type=models.CharField(max_length=10,choices=Ent_Type.choices,default=Ent_Type.PERSON)
    articles = models.ManyToManyField(Property, through='Sentiment')
"""    def __init__(self, arg):
        super(Entity, self).__init__()
        self.arg = arg"""

class Sentiment(models.Model):
    """docstring for Sentiment."""
    article=models.ForeignKey(Property, on_delete=models.CASCADE)
    entity=models.ForeignKey(Entity, on_delete=models.CASCADE)
    sentiment=models.BooleanField()
    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['article', 'entity'], name='only_one_result_for_article -entity')
        ]

class Wikipedia_url(models.Model):
    entity=models.ManyToManyField(Entity)
    url=models.CharField(max_length=500)
    def __init__(self, arg):
        super(Wikipedia_url, self).__init__()
        self.arg = arg
