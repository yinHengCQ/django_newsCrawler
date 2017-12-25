#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import re
# from crawler.models import news

def getNewsDiv():
    html=urllib2.urlopen('http://business.sohu.com/').read()
    soup=BeautifulSoup(html).html
    return str(soup.find_all('div',attrs={"data-newsid":not "","data-role":"news-item"}))

def getNewsTag_a():
    soup=BeautifulSoup(getNewsDiv())
    return str(soup.find_all('a',text=not ""))

def getNewsTitleList():
    content = BeautifulSoup(getNewsTag_a()).text.encode("utf-8").replace(' ','').replace('[','').replace(']','').replace("\r","").replace("\n","")
    # list=content.split(',$info.channelName,')
    print(content)
    list=re.split(r'\$info.channelName,',content)
    return list

def getNewsPublishList():
    pass

# def getTitleAndSave():
#     list=getNewsTitleList()
#     for var in list:
#         a=news()
#         a.title=var
#         a.save()

for var in getNewsTitleList():
    print(var)

