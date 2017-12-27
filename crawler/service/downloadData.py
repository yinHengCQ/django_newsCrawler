#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import re
from crawler.utils.dateUtil import int2date_YMDHMS
from crawler.models import news
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time



def getNewsDivList():
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")

    obj = webdriver.PhantomJS(executable_path='D:/python/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap)  # 加载网址
    obj.set_page_load_timeout(30)
    obj.get('http://business.sohu.com/')  # 打开网址
    try:
        soup = BeautifulSoup(obj.page_source).body
        list_str = str(soup.find_all('div', attrs={"data-newsid": not "", "data-role": "news-item"}))
        return list_str.split('</div>, <div')
    except Exception as e:
        print e
    finally:
        obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能
    # html=urllib2.urlopen('http://business.sohu.com/').read()
    # soup=BeautifulSoup(html).html
    # list_str= str(soup.find_all('div',attrs={"data-newsid":not "","data-role":"news-item"}))
    # return list_str.split('</div>, <div')

def getData():
    for var in getNewsDivList():
        soup = BeautifulSoup(var)

        # 获取标题
        title = unicode.encode(soup.h4.text, 'utf-8').replace('\n', '').replace('\r', '').replace(' ', '')

        # 获取Url
        url = unicode.encode('http:' + BeautifulSoup(str(soup.h4)).a.get("href"), 'utf-8')

        # 获取发布来源
        publisher = 'u'+unicode.encode(BeautifulSoup(str(soup.select('span[class="name"]'))).a.text, 'utf-8')

        #获取当前评论
        comment_count=unicode.encode(BeautifulSoup(str(soup.select('a[class="com"]'))).span.text, 'utf-8')

        # 获取发布时间
        pub_time = BeautifulSoup(str(soup.select('span[class="time"]'))).span.get('data-val')
        pub_date = int2date_YMDHMS(int(pub_time))

        #根据Url中的数字生成主键
        id = re.sub('\D', '', url)

        #保存数据
        # news.objects.update_or_create(id=id,title=title,url=url,publisher=publisher,comment_count=comment_count,pub_date=pub_date)
        try:
            orgin=news.objects.get(id=id)
            orgin.comment_count=comment_count
            orgin.save()
        except news.DoesNotExist:
            news.objects.create(id=id,title=title,url=url,publisher=publisher,comment_count=comment_count,pub_date=pub_date)


def saveData():
    try:
        getData()
    except Exception as e:
        print e

