#conding=uft-8
from django.shortcuts import render,render_to_response
from crawler.service.newsService import get_list_by_page
from crawler.service.crawlerManagerService import getCrawlerInfo
from crawler.service.outlook.job51Service import get_job51_list_by_page,get_job51_img
from django.http import HttpResponse
from django.core.cache import cache
# Create your views here.


def getIndex(request):
    return render(request,'index.html',{'list_state':getCrawlerInfo()})

def getData(request):
    return render(request,'showData.html',{'list_data':get_list_by_page(request)})

def getJob51Data(request):
    return render(request,'showJobData.html',{'list_data':get_job51_list_by_page(request)})

def getJobDataAnalysis(request):
    temp=cache.get('job51_need_list_list')
    result=[]
    for index in range(len(temp[0])):
        result.append({temp[0][index]:temp[1][index]})
    result.reverse()
    return render(request,'jobDataAnalysis.html',{'job51_need_list':result})

from crawler.test.job_detail_test import download
def test(request):
    download()
    return HttpResponse('ok')