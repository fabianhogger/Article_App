import requests
import pickle
import gensim

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render,redirect
from urllib.request import urlopen
from scraper.management.commands import crawl
from properties.models import Property,Library,Entity,Sentiment

from properties.trainlda import train_defs
from properties.preprocesslda import clean
from properties.extract_entities import process_for_ner
from properties.extract_sentiment import get_sentiment


import gensim.corpora as corpora
from gensim import models, similarities
from lxml import etree

from bs4 import BeautifulSoup as BSoup


def news_list(request):
    #print("news_list called")
    headlines=Property.objects.all()[0:10]
    context={
    'object_list':headlines
    }
    return render(request,"news.html",context)

def libraries(request):
    context=None
    if request.user.is_authenticated:
        mylibs=list(Library.objects.values_list('id','title').filter(user=request.user).order_by('title'))
        context={'library_names':mylibs}
    return render(request,'libraries.html',context)

def create_library(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            name=request.POST['name']
            print("NEW LIBRARY NAME ",name)
            print("user id ",request.user.id)

            if name != "":
                new_library=Library(title=name,user=request.user)
                new_library.save()
        mylibs=list(Library.objects.values_list('id','title').filter(user=request.user).order_by('title'))
        context={'library_names':mylibs}
    return render(request,'libraries.html',context)

def open_library(request,id):
    if request.user.is_authenticated:
        library_instance=Library.objects.filter(user=request.user,id=id)
        print(library_instance[0])
    return render(request,'mylib.html')

def add_to_lib(request,name,article):
    #get article id list and update it
    if request.user.is_authenticated:
        library_query=list(Library.objects.values_list('article_ids',flat=True).filter(user=request.user,title=name))
        lib=library_query
        #print(lib,type(lib))
    return render(request,'article.html')

def retrieve_article(request,name):
    named_entity_recognition(name)
    #update_viewcount(name)
    article_query=Property.objects.filter(name=name).values()
    context=article_query[0]
    similar_ids=context['similar_ids']
    similar=[]
    for sim_id in similar_ids:
        sim_article=Property.objects.values_list('name','image_url').filter(id=sim_id)
        similar.append(sim_article[0])
    context['similar']=similar
    if request.user.is_authenticated:
        mylibs=list(Library.objects.values_list('title',flat=True).filter(user=request.user).order_by('title'))
        context['library_names']=mylibs
    return render(request,'article.html',context)

def update_viewcount(name):
    article=Property.objects.filter(name=name)
    article[0]

def subm(request):
    return render(request,'subm.html')
def submit(request):
    if request.method=='POST':
        #print(request.POST['url'],request.POST['title'],request.POST['body'])
        url=request.POST['url']
        session=requests.Session()
        session.headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
        content=session.get(url,verify=True).content
        soup=BSoup(content,"html.parser")
        dom = etree.HTML(str(soup))
        print(dom.xpath('//title/text()')[0])
        #print(dom.xpath('//p/text()'))
        img_url=dom.xpath("//img/@src")[0]
        new_article=Property(name=dom.xpath('//title/text()')[0],body=' '.join(dom.xpath('//p/text()')),url=url,image_url=img_url)
        new_article.save()
        named_entity_recognition(new_article.name)
        #img_temp = NamedTemporaryFile()
        #img_temp.write(urlopen(img_url).read())
        #img_temp.flush()
        #new_article.image_file.save("image_%s" % new_article.pk, File(img_temp))
        #new_article.save()
        return render(request,'subm.html')
    else:
        print('ERROR WITH FORM')
        return render(request,'subm.html')
def images(request):
    all_urls=Property.objects.values_list('url', flat=True).filter(image_file='default.jpg')
    #print(len(all_urls))
    for url in all_urls:
        #print(url)
        session=requests.Session()
        session.headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
        content=session.get(url,verify=True).content
        soup=BSoup(content,"html.parser")
        dom = etree.HTML(str(soup))
        image_url=dom.xpath("//img/@src")[0]
        if len(image_url)<700:
            if image_url[0]=='/':
                if  'bbc' in url:
                    image_url=requests.compat.urljoin('https://www.bbc.com/', image_url)
                else:
                    image_url=requests.compat.urljoin('https://www.aljazeera.com/', image_url)
            queryobject=Property.objects.filter(url=url).update(image_url=image_url)
            img_temp = NamedTemporaryFile()
            img_temp.write(urlopen(image_url).read())
            img_temp.flush()
            object=Property.objects.filter(url=url)
            for obj in object:
                print(obj.image_file)
                obj.image_file.save("image_%s" % obj.pk, File(img_temp))
                print(obj.image_file)
                obj.save()
    return render(request,'news.html')

def topics(request):
    return render(request,'topics.html')

def scrape(request):
    pass
def train(request):
    corpus=Property.objects.values_list('id','body').order_by('id')
    train_defs.start(list(corpus))
    return redirect("news")
def get_similar(request):
    lda=gensim.models.ldamodel.LdaModel.load('properties/lda/lda_15_articles_wlist/model15bodies')
    all_ids=Property.objects.values_list('id' ,flat=True).order_by('id')
    #print(all_ids)
    with open('properties/lda/lda_15_articles_wlist/list_ids15.pkl', 'rb') as f:
        ids = pickle.load(f)
    ids=list(ids)
    #print(ids)
    for j in all_ids:
        queryobject=Property.objects.filter(id=j).values()
        dic=queryobject[0]
        if  not dic['similar_ids']:
            body=[]
            body.append(dic['body'])
            clean_body=clean.clean_text(body)
            vector1=lda[clean_body[0]]
            sims=clean.get_similarity(lda,vector1)
            #sims=clean.get_jensen_shannon(lda,vector1)
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            tens=sims[:10]
            articles=[]
            for i in range(10):
                index=tens[i][0]
                id_=ids[index]
                articles.append(id_)
                Property.objects.filter(id=j).update(similar_ids=articles)
    return render(request,'news.html')

def named_entity_recognition(name):
    text_body =Property.objects.filter(name=name).values_list('body',flat=True)
    Article_instance = Property.objects.get(name=name)
    #print(text_body[0])
    entities,types=process_for_ner(text_body[0])
    #print(types)
    for ent in entities.keys():
            #print(type(ent))
            #returns tuple with object and boolean created
            new_entity=Entity.objects.get_or_create(name=ent,type=types[ent])
            sentiment=get_sentiment(entities[ent])
            sent_inst=Sentiment.objects.get_or_create(article=Article_instance,entity=new_entity[0],sentiment=sentiment)
