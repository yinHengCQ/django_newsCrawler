#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
# import time
import re
# from crawler.utils.dateUtil import int2date_YMDHMS
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
# import threading
# import random
# from crawler.utils.disguiseUtil import getRandomUserAgent



# def getNewsDivList():
#     dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
#     dcap["phantomjs.page.settings.userAgent"] = getRandomUserAgent()
#
#
#     obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap)  # 加载网址
#     obj.set_page_load_timeout(10)
#     obj.get('http://127.0.0.1:8080/SSH_Demo_Maven/showAll.do')  # 打开网址
#     try:
#         soup = BeautifulSoup(obj.page_source).body
#         print soup
#         # list_str = str(soup.find_all('div', attrs={"data-newsid": not "", "data-role": "news-item"}))
#         # return list_str.split('</div>, <div')
#     except Exception as e:
#         print e
#     obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能

# html=urllib2.urlopen('http://business.sohu.com/').read()
# soup=BeautifulSoup(html).html
# list_str= str(soup.find_all('div',attrs={"data-newsid":not "","data-role":"news-item"}))
# return list_str.split('</div>, <div')


# for var in getNewsDivList():
#     soup = BeautifulSoup(var)
#     result=unicode.encode(BeautifulSoup(str(soup.select('a[class="com"]'))).span.text, 'utf-8')
#     print('*'*50)
#     print(type(result))
#     print(result)

# def print_task():
#     try:
#         print 10 / random.choice([0, 1, 2, 3])
#     except Exception as e:
#         print e
#     threading.Timer(random.randint(1,4),print_task).start()

# threading.Timer(2,print_task).start()

# def __get_crawler(default_referer):
#     return dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent

# proxy=webdriver.Proxy()
# proxy.proxy_type=ProxyType.MANUAL
# proxy.http_proxy='171.35.103.37:808'
# proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)


def get_proxy_ip_data(responseBody):
    list= str(responseBody.find_all('tr','odd')).split(',')
    for var in list:
        print('*'*100)
        list_str=BeautifulSoup(var).find_all('td')

        try:
            ip = str(list_str[1].text)  # 获取代理IP
            port = str(list_str[2].text).replace('\n', '').replace('\r', '').replace(' ', '')  # 获取端口号
            address = BeautifulSoup(list_str[3].text).text.replace('\n', '').replace('\r', '').replace(' ',
                                                                                                       '')  # 获取服务器地址
            # address=unicode(str(address),'unicode-escape').replace('\n', '').replace('\r', '').replace(' ', '')
            type = str(list_str[5].text)  # 获取类型
            id = ip + port  # 生成id
            response_time = BeautifulSoup(str(list_str[6])).div['title']
            print(response_time)
            aa=re.sub(u'秒', '',response_time)
            aaa=float(aa)
            print(aaa)
            print aaa<1
        except Exception as e:
            print e

dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap["phantomjs.page.settings.userAgent"] = "MQQBrowser/25 (Linux; U; 2.3.3; zh-cn; HTC Desire S Build/GRI40;480*800)"
# service_args=['--proxy=42.84.231.99:80']

obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap)
# obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap,service_args=service_args)  # 加载网址
obj.set_page_load_timeout(10)
# obj.get('http://101.201.235.99:8080/springmvc_hibernate_demo/showAll.do')  # 打开网址
obj.get('https://www.baidu.com/')
try:
    soup = BeautifulSoup(obj.page_source).body
    print soup
    # get_proxy_ip_data(soup)
except Exception as e:
    print e
finally:
    obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能




