#conding=uft-8
from django.shortcuts import render
from service.downloadData import getTitleAndSave,test
from django.http import HttpResponse

# Create your views here.

def getTitleSave(request):
    getTitleAndSave()
    return HttpResponse('OK')