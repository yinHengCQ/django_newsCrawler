#conding=uft-8
from django.shortcuts import render
from crawler.service.newsService import get_list_by_page
from crawler.service.crawlerManagerService import getCrawlerInfo
from crawler.service.downloadData_test import ttt
from django.http import HttpResponse
# Create your views here.


def getIndex(request):
    return render(request,'index.html',{'list_state':getCrawlerInfo()})

def getData(request):
    return render(request,'showData.html',{'list_data':get_list_by_page(request)})

def gettt(request):
    ttt()
    return HttpResponse('ok')