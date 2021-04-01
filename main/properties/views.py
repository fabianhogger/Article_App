from django.shortcuts import render,redirect
from scraper.management.commands import crawl
from properties.models import Property
from properties.train import train_defs
from properties.preprocess import clean

import gensim
import gensim.corpora as corpora
from gensim import models, similarities


def news_list(request):
    print("news_list called")
    headlines=Property.objects.all()[:10]
    context={
    'object_list':headlines
    }
    return render(request,"news.html",context)

def scrape(request):
    pass
def train(request):
    corpus=Property.objects.values_list('name')
    corpus_aslist=[tupleitem for item in corpus for tupleitem in item]
    #print((corpus_aslist[11]))
    train_defs.start(corpus_aslist)
    return redirect("news")

def get_similar(request):
    lda=gensim.models.ldamodel.LdaModel.load('properties/lda/lda2450_30/model30')
    for j in range(1501,1504):
        queryobject=Property.objects.filter(id=j).values()
        dic=queryobject[0]
        body=[]
        body.append(dic['body'])
        #print("DATA BEFORE ANYTHING",body[0])
        clean_body=clean.clean_text(body)
        #print('clean body',clean_body[0])
        vector1=lda[clean_body[0]]
        #sims=clean.get_similarity(lda,vector1)
        sims=clean.get_jensen_shannon(lda,vector1)
        print("ENUMERATED  ",enumerate(sims))
        sims = sorted(enumerate(sims), key=lambda item: item[1])
        tens=sims[:10]
        articles=[]
        all_ids=Property.objects.values_list('id')
        all_ids=[tupleitem for item in all_ids for tupleitem in item]
        print(all_ids)
        for i in range(10):
            id_=tens[i][0]
            print('OK ',id_)
            if id_ in all_ids:
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
