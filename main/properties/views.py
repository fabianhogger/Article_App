from django.shortcuts import render
from scraper.management.commands import crawl
from properties.models import Property


def news_list(request):
    print("news_list called")
    headlines=Property.objects.all()[:10]
    context={
    'object_list':headlines
    }
    return render(request,"news.html",context)

def scrape(request):
    pass
def train_lda(request):
    
