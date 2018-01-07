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


###################################################################################################################
# def get_proxy_ip_data(responseBody):
#     list= str(responseBody.find_all('tr','odd')).split(',')
#     for var in list:
#         print('*'*100)
#         list_str=BeautifulSoup(var).find_all('td')
#
#         try:
#             ip = str(list_str[1].text)  # 获取代理IP
#             port = str(list_str[2].text).replace('\n', '').replace('\r', '').replace(' ', '')  # 获取端口号
#             address = BeautifulSoup(list_str[3].text).text.replace('\n', '').replace('\r', '').replace(' ',
#                                                                                                        '')  # 获取服务器地址
#             # address=unicode(str(address),'unicode-escape').replace('\n', '').replace('\r', '').replace(' ', '')
#             type = str(list_str[5].text)  # 获取类型
#             id = ip + port  # 生成id
#             response_time = BeautifulSoup(str(list_str[6])).div['title']
#             print(response_time)
#             aa=re.sub(u'秒', '',response_time)
#             aaa=float(aa)
#             print(aaa)
#             print aaa<1
#         except Exception as e:
#             print e
#
# dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
# dcap["phantomjs.page.settings.userAgent"] = "MQQBrowser/25 (Linux; U; 2.3.3; zh-cn; HTC Desire S Build/GRI40;480*800)"
# # service_args=['--proxy=42.84.231.99:80']
#
# obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap)
# # obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap,service_args=service_args)  # 加载网址
# obj.set_page_load_timeout(10)
# # obj.get('http://101.201.235.99:8080/springmvc_hibernate_demo/showAll.do')  # 打开网址
# obj.get('https://www.baidu.com/')
# try:
#     soup = BeautifulSoup(obj.page_source).body
#     print soup
#     # get_proxy_ip_data(soup)
# except Exception as e:
#     print e
# finally:
#     obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能
###################################################################################################################

from crawler.models import job51

def salary_unicode2int(salary):
    list_temp=salary.replace('千'.decode('utf-8'),'').replace('月'.decode('utf-8'),'').replace('万'.decode('utf-8'),'').replace('年'.decode('utf-8'),'').replace('/','').split('-')
    if salary.find('月'.decode('utf-8'))>0:
        if salary.find('千'.decode('utf-8'))>0:
            low=int(float(list_temp[0])*1000)
            high=int(float(list_temp[1])*1000)
        elif salary.find('万'.decode('utf-8'))>0:
            low = int(float(list_temp[0]) * 10000)
            high = int(float(list_temp[1]) * 10000)
        return {'low':low,'high':high}
    elif salary.find('年'.decode('utf-8'))>0:
        low = int(float(list_temp[0]) * 10000)/12
        high = int(float(list_temp[1]) * 10000)/12
        return {'low':low,'high':high}

def get_proxy_ip_data(responseBody):
    list= str(responseBody).replace('</a><a','</a>,<a').split(',')
    for var in list:
        soup=BeautifulSoup(var)

        job_name = soup.h3.text
        job_url = soup.a.get('href')
        company_name = soup.aside.text
        job_address = soup.i.text
        job_salary = soup.em.text
        salary_temp = salary_unicode2int(job_salary)
        salary_low = salary_temp.get('low')
        salary_high = salary_temp.get('high')
        id=soup.b.get('value')

        try:
            job51.objects.update_or_create(id=id,job_name=job_name,job_url=job_url,company_name=company_name,
                job_address=job_address,job_salary=job_salary,salary_low=salary_low,salary_high=salary_high)
        except Exception as e:
            print e




def ttt():
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap[
        "phantomjs.page.settings.userAgent"] = "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10"
    # service_args=['--proxy=42.84.231.99:80']

    obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe',
                              desired_capabilities=dcap)
    # obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap,service_args=service_args)  # 加载网址
    obj.set_page_load_timeout(10)
    # obj.get('http://101.201.235.99:8080/springmvc_hibernate_demo/showAll.do')  # 打开网址
    # obj.get('http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,1.html')
    obj.get('http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,1.html')
    try:
        soup = BeautifulSoup(obj.page_source)
        content = soup.select('.items')
        get_proxy_ip_data(content)
    except Exception as e:
        print e
    finally:
        obj.quit()
