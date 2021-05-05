from django.shortcuts import render,redirect
from scraper.management.commands import crawl
from properties.models import Property
from properties.train import train_defs
from properties.preprocess import clean

import pickle
import gensim
import gensim.corpora as corpora
from gensim import models, similarities
from lxml import etree
import requests
from bs4 import BeautifulSoup as BSoup
from properties.models import Property

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
def news_list(request):
    print("news_list called")
    headlines=Property.objects.all()[:10]
    context={
    'object_list':headlines
    }
    return render(request,"news.html",context)
def libraries(request):
    return render(request,'libraries.html')

def retrieve_article(request,name):
    article_query=Property.objects.filter(name=name).values()
    context=article_query[0]
    similar_ids=context['similar_ids']
    similar=[]
    for sim_id in similar_ids:
        sim_article=Property.objects.values_list('name','image_file').filter(id=sim_id)
        similar.append(sim_article[0])
    context['similar']=similar
    return render(request,'article.html',context)

def subm(request):
    return render(request,'subm.html')
def submit(request):
    if request.method=='POST':
        print(request.POST['url'],request.POST['title'],request.POST['body'])
        url=request.POST['url']
        session=requests.Session()
        session.headers={"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
        content=session.get(url,verify=True).content
        soup=BSoup(content,"html.parser")
        dom = etree.HTML(str(soup))
        print(dom.xpath('//title/text()')[0])
        print(dom.xpath('//p/text()'))
        img_url=dom.xpath("//img/@src")[0]
        new_article=Property(name=dom.xpath('//title/text()')[0],body=' '.join(dom.xpath('//p/text()')),url=url,image_url=img_url)
        new_article.save()
        img_temp = NamedTemporaryFile()
        img_temp.write(urlopen(img_url).read())
        img_temp.flush()
        new_article.image_file.save("image_%s" % new_article.pk, File(img_temp))

        new_article.save()
        return render(request,'subm.html')
    else:
        print('ERROR WITH FORM')
        return render(request,'subm.html')
def images(request):
    all_urls=Property.objects.values_list('url', flat=True).filter(image_file='default.jpg')
    print(len(all_urls))
    for url in all_urls:
        print(url)
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
    print(all_ids)
    with open('properties/lda/lda_15_articles_wlist/list_ids15.pkl', 'rb') as f:
        ids = pickle.load(f)
    ids=list(ids)
    print(ids)
    for j in ids:
        queryobject=Property.objects.filter(id=j).values()
        dic=queryobject[0]
        body=[]
        body.append(dic['body'])
        clean_body=clean.clean_text(body)
        #print(clean_body[0])
        vector1=lda[clean_body[0]]
        sims=clean.get_similarity(lda,vector1)
        #sims=clean.get_jensen_shannon(lda,vector1)
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        tens=sims[:10]
        #print(tens)
        articles=[]
        for i in range(10):
            index=tens[i][0]
            id_=ids[index]
            articles.append(id_)
        print('articles',articles)
        print('type',type(articles[0]))
        Property.objects.filter(id=j).update(similar_ids=articles)

    return render(request,'news.html')


"""
def update_lda(article_body):
        pass
    cleaned=clean(article_body)
    lda=load_lda()
    lda.update(cleaned)
"""
