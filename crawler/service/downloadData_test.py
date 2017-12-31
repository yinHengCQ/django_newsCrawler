#coding=utf-8
# import urllib2
# from bs4 import BeautifulSoup
# import time
# import re
# from crawler.utils.dateUtil import int2date_YMDHMS
# from selenium import webdriver
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
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

a= '\u8bc1\u76d1\u4f1a\uff1a\u9ad8\u5ea6\u91cd\u89c6\u884c'
print unicode(a,'unicode-escape')
