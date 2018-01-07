#conding=uft-8
from django.shortcuts import render
from crawler.service.newsService import get_list_by_page
from crawler.service.crawlerManagerService import getCrawlerInfo
from crawler.service.outlook.job51Service import get_job51_list_by_page
# Create your views here.


def getIndex(request):
    return render(request,'index.html',{'list_state':getCrawlerInfo()})

def getData(request):
    return render(request,'showData.html',{'list_data':get_list_by_page(request)})

def getJob51Data(request):
    return render(request,'showJobData.html',{'list_data':get_job51_list_by_page(request)})