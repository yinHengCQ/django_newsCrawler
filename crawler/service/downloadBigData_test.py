#coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap[
    "phantomjs.page.settings.userAgent"] = "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"
# service_args=['--proxy=42.84.231.99:80']

obj = webdriver.Chrome(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', desired_capabilities=dcap)
# obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap,service_args=service_args)  # 加载网址
obj.set_page_load_timeout(10)
# obj.get('http://101.201.235.99:8080/springmvc_hibernate_demo/showAll.do')  # 打开网址
# obj.get('http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,1.html')
obj.get('http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,1.html')
try:
    soup = BeautifulSoup(obj.page_source).select('#resultList')
    content = BeautifulSoup(str(soup)).find_all('div','el')
    # get_proxy_ip_data(content)
    print content
except Exception as e:
    print e
finally:
    obj.quit()

