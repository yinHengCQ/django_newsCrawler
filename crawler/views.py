#conding=uft-8
from django.shortcuts import render
from service.downloadData import saveData
from django.http import HttpResponse

# Create your views here.

def getTitleSave(request):
    saveData()
    return HttpResponse('OK')