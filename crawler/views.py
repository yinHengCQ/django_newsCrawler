#conding=uft-8
from django.shortcuts import render
from django.http import HttpResponse
from crawler.task.crawlerTask import newsCrawle
from crawler.service.newsService import get_list_by_page

# Create your views here.

def getTitleSave(request):
    newsCrawle()
    return HttpResponse('OK')

def getIndex(request):
    return render(request,'index.html')

def getData(request):
    return render(request,'showData.html',{'list_data':get_list_by_page(request)})