from django.shortcuts import render,redirect
from scraper.management.commands import crawl
from properties.models import Property
from properties.train import train_defs
from properties.preprocess import clean

import gensim
import gensim.corpora as corpora
from gensim import models, similarities

import pickle
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
    article=article_query[0]
    print(article)
    context={
    'object_list':article_query
    }
    return render(request,'article.html',context)

def subm(request):
    return render(request,'subm.html')
def submit(request):
    if request.method=='POST':
        print(request.POST['url'],request.POST['title'],request.POST['body'])
        return render(request,'subm.html')
    else:
        print('ERROR WITH FORM')
        return render(request,'subm.html')
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
    all_ids=Property.objects.values_list('id' ,flat=True)
    print(all_ids)
    for j in range(230,233):
        if j in all_ids:
            queryobject=Property.objects.filter(id=j).values()
            dic=queryobject[0]
            body=[]
            body.append(dic['body'])
            clean_body=clean.clean_text(body)
            vector1=lda[clean_body[0]]
            sims=clean.get_similarity(lda,vector1)
            #sims=clean.get_jensen_shannon(lda,vector1)
            sims = sorted(enumerate(sims), key=lambda item: -item[1])
            tens=sims[:10]
            with open('properties/lda/lda_15_articles_wlist/list_ids15.pkl', 'rb') as f:
                ids = pickle.load(f)
            ids=list(ids)
            articles=[]
            for i in range(10):
                index=tens[i][0]
                id_=ids[index]
                queryobject_article=Property.objects.filter(id=id_).values()
                similar_article=queryobject_article[0]#getting the dictionary from the object
                articles.append(similar_article['name'])
            print('initial article',dic['name'])
            print(articles)
    return redirect("news")


"""
def update_lda(article_body):
        pass
    cleaned=clean(article_body)
    lda=load_lda()
    lda.update(cleaned)
"""
