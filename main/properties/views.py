from django.shortcuts import render,redirect
from scraper.management.commands import crawl
from properties.models import Property
from properties.train import train_defs

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
    corpus=Property.objects.values_list('body')
    corpus_aslist=[tupleitem for item in corpus for tupleitem in item]
    #print((corpus_aslist[11]))
    train_defs.start(corpus_aslist)
    return redirect("news")
"""
def update_lda(article_body):
        pass
    cleaned=clean(article_body)
    lda=load_lda()
    lda.update(cleaned)
"""
