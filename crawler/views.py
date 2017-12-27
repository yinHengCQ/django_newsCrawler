#conding=uft-8
from django.shortcuts import render
from service.downloadData import saveData
from django.http import HttpResponse
from crawler.task.crawlerTask import newsCrawle

# Create your views here.

def getTitleSave(request):
    # saveData()
    newsCrawle()
    return HttpResponse('OK')