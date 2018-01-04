#coding=utf-8
from bs4 import BeautifulSoup
from crawler.utils.dateUtil import int2date_YMDHMS
from crawler.utils.disguiseUtil import getRandomUserAgent,getRandomReferer
from crawler.models import news,proxyIP
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging,threading,time,re
from django.core.cache import cache
from crawler.service.browserService import check_browser_state,save_browser_close_state,save_browser_open_state



logger=logging.getLogger('django')

def __get_task_list():
    try:
        return cache.get('task_list')
    except Exception as e:
        logger.error(u'获取爬虫任务列表异常：'+e.message)

def __run(list_task):
    cache.set('task_list',[])
    check_browser_state()
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = getRandomUserAgent()
    dcap["phantomjs.page.settings.referer"]=getRandomReferer()
    try:
        # obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe',
        #                           desired_capabilities=dcap)  # 加载网址
        obj = webdriver.PhantomJS(executable_path='/root/phantomjs/bin/phantomjs',desired_capabilities=dcap)  # 加载网址
        obj.set_page_load_timeout(10)
        logger.info(u'开始抓取网页数据...')
        for task_name in list_task:
            if task_name=='newsCrawler':
                key='http://business.sohu.com/'
                obj.get(key)
                threading._start_new_thread(__save_news_data,(key,BeautifulSoup(obj.page_source).body,))
                time.sleep(5)
            elif task_name=='proxyIpCrawler':
                key='http://www.xicidaili.com/nn/'
                obj.get(key)
                threading._start_new_thread(__save_proxy_ip_data,(key,BeautifulSoup(obj.page_source).body,))
                time.sleep(5)
    except Exception as e:
        logger.error(u'下载网页数据时异常:' + e.message)
    finally:
        save_browser_open_state()
        obj.quit()
        save_browser_close_state()



def __get_news_data(key,responseBody):
    list_str = str(responseBody.find_all('div', attrs={"data-newsid": not "", "data-role": "news-item"}))
    for var in list_str.split('</div>, <div'):
        # soup=BeautifulSoup(var)
        soup = BeautifulSoup(unicode(var,'unicode-escape'))

        # 获取标题
        title = unicode.encode(soup.h4.text, 'utf-8').replace('\n', '').replace('\r', '').replace(' ', '')

        # 获取Url
        url = unicode.encode('http:' + BeautifulSoup(str(soup.h4)).a.get("href"), 'utf-8')

        # 获取发布来源
        publisher = unicode.encode(BeautifulSoup(str(soup.select('span[class="name"]'))).a.text, 'utf-8')
        publisher = unicode(publisher, 'unicode-escape')

        #获取当前评论
        comment_count=unicode.encode(BeautifulSoup(str(soup.select('a[class="com"]'))).span.text, 'utf-8')
        comment_count = unicode(comment_count, 'unicode-escape')

        # 获取发布时间
        pub_time = BeautifulSoup(str(soup.select('span[class="time"]'))).span.get('data-val')
        pub_date = int2date_YMDHMS(int(pub_time))

        #根据Url中的数字生成主键
        id = re.sub('\D', '', url)

        try:
            orgin=news.objects.get(id=id)
            orgin.comment_count=comment_count
            orgin.save()
        except news.DoesNotExist:
            news.objects.create(id=id,title=title,url=url,publisher=publisher,comment_count=comment_count,pub_date=pub_date)

def __save_news_data(key,responseBody):
    try:
        __get_news_data(key,responseBody)
    except Exception as e:
        logger.error(u'抓取并保存新闻数据异常：'+e.message)


def __get_proxy_ip_data(key,responseBody):
    list= str(responseBody.find_all('tr','odd')).split(',')
    for var in list:
        list_str=BeautifulSoup(var).find_all('td')

        ip=str(list_str[1].text) #获取代理IP
        port=str(list_str[2].text).replace('\n', '').replace('\r', '').replace(' ', '') #获取端口号
        address=BeautifulSoup(list_str[3].text).text.replace('\n', '').replace('\r', '').replace(' ', '')#获取服务器地址
        type=str(list_str[5].text) #获取类型
        id=ip+port #生成id

        try:
            proxyIP.objects.update_or_create(id=id,ip_address=ip,ip_port=port,address=address,ip_type=type,source=key)
        except Exception as e:
            logger.error(u'保存代理Ip异常：'+e.message)

def __save_proxy_ip_data(key):
    try:
        __get_proxy_ip_data(key)
    except Exception as e:
        logger.error(u'抓取并保存代理IP数据异常'+e.message)

def startCrawler():
    list_task=__get_task_list()
    if len(list_task)==0:
        logger.info(u'本次任务结束，没有需要执行的爬虫任务')
    else:
        __run(list_task)
        logger.info(u'本次爬虫任务完成')
