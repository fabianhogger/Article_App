import requests
import pickle
import gensim
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import render,redirect
from urllib.request import urlopen
from scraper.management.commands import crawl
from properties.models import Property,Library,Entity,Sentiment,Wikipedia_url

from properties.trainlda import train_defs
from properties.preprocesslda import clean
from properties.extract_entities import process_for_ner
from properties.extract_sentiment import get_sentiment


import gensim.corpora as corpora
from gensim import models, similarities
from lxml import etree

from bs4 import BeautifulSoup as BSoup
from django.db import connection
import re
def news_list(request):
    #print("news_list called")
    headlines=Property.objects.order_by('date')[:30]
    print(headlines)
    headl=[]
    for item in headlines:
        if item.image_url!="www.noimage.com":
            headl.append(item)
    Topvideo=Property.objects.all().order_by('-views')[:1]
    print(Topvideo[0])
    context={
    'Topvideo':Topvideo,
    'object_list':headl,
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
    context={}
    if request.user.is_authenticated:
        opened_lib=Library.objects.get(user=request.user,id=id)
        articles=list(opened_lib.article_ids.all())
        context['article_names']=articles
        context['library']=opened_lib
    return render(request,'mylib.html',context)

def add_to_lib(request,name,id):
    #get article id list and update it
    if request.user.is_authenticated:
        mylib=Library.objects.get(user=request.user,title=name)
        Article=Property.objects.get(id=id)
        mylib.article_ids.add(Article)
        mylib.save()
        print(mylib)
    return retrieve_article(request,id)
def delete_library(request,id):
    if request.user.is_authenticated:
        mylib=Library.objects.filter(user=request.user,id=id).delete()
    return libraries(request)

def retrieve_article(request,id):
    #scan_all_entities()
    update_viewcount(id)
    article_query=Property.objects.filter(id=id).values()
    context=article_query[0]
    similar_ids=context['similar_ids']
    similar=[]
    for sim_id in similar_ids:
        sim_article=Property.objects.values_list('name','image_url','id').filter(id=sim_id)
        similar.append(sim_article[0])
    context['similar']=similar
    if request.user.is_authenticated:
        mylibs=list(Library.objects.values_list('title',flat=True).filter(user=request.user).order_by('title'))
        context['library_names']=mylibs
        #print(context)
    return render(request,'article.html',context)

def update_viewcount(id):
    article_views=Property.objects.values_list('views',flat=True).filter(id=id)
    article_views=article_views[0]+1
    Property.objects.filter(id=id).update(views=article_views)

def subm(request):
    return render(request,'subm.html')
def submit(request):
    print(request.POST)
    if request.method=='POST' and request.POST.get('title') is None:
        print("entered URL SUBMIT")
        url=request.POST['url']
        session=requests.Session()
        session.headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
        content=session.get(url,verify=True).content
        soup=BSoup(content,"html.parser")
        dom = etree.HTML(str(soup))
        #print(dom.xpath('//title/text()')[0])
        #print(dom.xpath('//p/text()'))
        img_url=dom.xpath("//img/@src")[0]
        source = re.sub(".com(.*)",'', url)
        source = re.sub("(.*)www.",'', source)
        context={'name':dom.xpath('//title/text()')[0],'body':' '.join(dom.xpath('//p/text()')),'url':url,'image_url':dom.xpath("//img/@src")[0],'source':source}
        return render(request,'subm.html',context)
        #new_article=Property(name=dom.xpath('//title/text()')[0],body=' '.join(dom.xpath('//p/text()')),url=url,image_url=img_url)
        #new_article.save()
        #named_entity_recognition(new_article.id)
        #return render(request,'subm.html')
    elif request.POST.get('title'):
            new_article=Property(name=request.POST['title'],body=request.POST['body'],url=request.POST['url'],image_url=request.POST['image_url'])
            print("SAVING ARTICLEEEEEEEE")
            new_article.save()
            similar=find_similar(request.POST['body'])
            Property.objects.filter(id=new_article.id).update(similar_ids=similar)
            named_entity_recognition(new_article.id)
            #retrieve computed entities
            cursor=connection.cursor()
            query="select t1.entity_id,t2.name from properties_sentiment as t1,properties_entity as t2 where article_id={} and t1.entity_id=t2.id".format(new_article.id)
            cursor.execute(query,['localhost'])
            entities=cursor.fetchall()
            #entities=[item[1] for item in entities]
            print(entities)
            context={'entities':entities}
            return render(request,'subm.html',context)
    else:
        print('ERROR WITH FORM')
        return render(request,'subm.html')

def find_similar(bod):
    lda=gensim.models.ldamodel.LdaModel.load('properties/lda/lda_15_articles_wlist/model15bodies')
    all_ids=Property.objects.values_list('id' ,flat=True).order_by('id')
    with open('properties/lda/lda_15_articles_wlist/list_ids15.pkl', 'rb') as f:
        ids = pickle.load(f)
    ids=list(ids)
    body=[]
    body.append(bod)
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
    #Property.objects.filter(id=j).update(similar_ids=articles)
    return articles
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
    cursor=connection.cursor()
    places="select count(*)-count(*) filter (where t1.sentiment),count(*) filter (where t1.sentiment),t2.name from properties_sentiment as t1,properties_entity as t2 where t1.entity_id = t2.id and t2.type like 'GPE' group by t2.name,t2.type order by count(t1.sentiment) DESC"
    cursor.execute(places, ['localhost'])
    places= cursor.fetchall()
    people="select count(*)-count(*) filter (where t1.sentiment),count(*) filter (where t1.sentiment),t2.name from properties_sentiment as t1,properties_entity as t2 where t1.entity_id = t2.id and t2.type like 'PERSON' group by t2.name,t2.type order by count(t1.sentiment) DESC"
    cursor.execute(people, ['localhost'])
    people= cursor.fetchall()
    orgs="select count(*)-count(*) filter (where t1.sentiment),count(*) filter (where t1.sentiment),t2.name from properties_sentiment as t1,properties_entity as t2 where t1.entity_id = t2.id and t2.type like 'ORG' group by t2.name,t2.type order by count(t1.sentiment) DESC"
    cursor.execute(orgs, ['localhost'])
    orgs= cursor.fetchall()
    ##entities= Entity.objects.values_list('name','type').order_by('articles')
    context={"people":people[:50],"places":places[:50],"orgs":orgs[:50]}
    return render(request,'topics.html',context)


def scrape(request):
    pass
def train(request):
    corpus=Property.objects.values_list('id','body').order_by('id')
    train_defs.start(list(corpus))
    return redirect("news")

def whoweare(request):
    return render(request,"Whoweare.html")
def get_similar(request):
    '''
    all_ids=Property.objets.values_list('id','url' ).order_by('id')
    for j  in range(len(all_ids)):
        tu=all_ids[j]
        x = re.sub(".com(.*)",'', tu[1])
        print(x)
        x = re.sub("(.*)www.",'', x)
        print(x)
        Property.objects.filter(id=tu[0]).update(source=x)
    #    queryobject=Property.objects.get(id=j).values(
    '''
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
def scan_all_entities():
    already=[87,4,51,96,52,1748,67,132,1050,1741,1750,39,92,605,513,93,89,541,1051,69,292,50,102,14,22,59,1776,1745,65,16,75,577,630,11,1704,99,805,1758,534,41,46,1773,808,53,32,214,7,658,649,358,100,1753,48,12,532,85,72,57,24,81,77,519,1769,1124,49,1763,508,671,37,901,20,1,18,55,813,1752,58,809,8]
    ids=list(Property.objects.values_list('id',flat=True))
    ids=[id for id in ids if id not in already]
    for id in ids:
        named_entity_recognition(id)
        print('Done ', id)
def named_entity_recognition(id):
    text_body =Property.objects.filter(id=id).values_list('body',flat=True)
    Article_instance = Property.objects.get(id=id)
    entities,types,urls=process_for_ner(text_body[0])
    for ent in entities.keys():
            #returns tuple with object and boolean created
            try:
                new_entity=Entity.objects.get_or_create(name=ent,type=types[ent])
                sentiment=get_sentiment(entities[ent])
                Sentiment.objects.get_or_create(article=Article_instance,entity=new_entity[0],sentiment=sentiment)
                for url in urls[ent]:
                    if url is not None:
                        wiki=Wikipedia_url.objects.get_or_create(url=url)
                        wiki[0].entity.add(new_entity[0])
            except:
                pass
def view_entity_data(request,ent_id):
    cursor=connection.cursor()
    entity_data="select t1.id,t1.name,t2.sentiment,t1.source from properties_property as t1,properties_sentiment as t2,properties_entity as t3 where t2.article_id=t1.id and t2.entity_id={id} and t3.id={id}".format(id=ent_id)
    cursor.execute(entity_data, ['localhost'])
    entity_data= cursor.fetchall()
    ent="select name from properties_entity where id={id}".format(id=ent_id)
    cursor.execute(ent, ['localhost'])
    entity=cursor.fetchall()
    context={"entity_data":entity_data,"entity_name":entity}
    print(entity)
    return render(request,'entity.html',context)
