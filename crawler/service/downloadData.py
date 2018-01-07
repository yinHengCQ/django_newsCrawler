#coding=utf-8
from bs4 import BeautifulSoup
from crawler.utils.dateUtil import int2date_YMDHMS
from crawler.utils.disguiseUtil import getRandomPCUserAgent,getRandomReferer
from crawler.utils.strUtil import salary_unicode2int
from crawler.models import news,proxyIP,job51
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging,threading,time,re,random
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
    dcap["phantomjs.page.settings.userAgent"] = getRandomPCUserAgent()
    dcap["phantomjs.page.settings.referer"]=getRandomReferer()
    # service_args=['--proxy=42.84.231.99:80']
    try:
        obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe',
                                  desired_capabilities=dcap)  # 加载网址
        # obj = webdriver.PhantomJS(executable_path='/root/phantomjs/bin/phantomjs',desired_capabilities=dcap)  # 加载网址
        # obj = webdriver.PhantomJS(executable_path='C:/Users/Administrator/phantomjs/bin/phantomjs.exe', desired_capabilities=dcap,service_args=service_args)  # 加载网址
        obj.set_page_load_timeout(15)
        logger.info(u'开始抓取网页数据...')
        for task_name in list_task:
            if task_name=='newsCrawler':
                key='http://business.sohu.com/'
                obj.get(key)
                threading._start_new_thread(__save_news_data,(key,BeautifulSoup(obj.page_source).body,))
            elif task_name=='proxyIpCrawler':
                key='http://www.xicidaili.com/nn/'
                obj.get(key)
                threading._start_new_thread(__save_proxy_ip_data,(key,BeautifulSoup(obj.page_source).body,))
            elif task_name=='job51Crawler':
                page=cache.get('job51Crawler_page')
                if page==None:
                    key = 'http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,1.html'
                    cache.set('job51Crawler_page','1')
                elif page=='2000':
                    key = 'http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,1.html'
                    cache.set('job51Crawler_page','1')
                else:
                    key = 'http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,'+str(int(page)+1)+'.html'
                    cache.set('job51Crawler_page',str(int(page)+1))
                time.sleep(random.randint(0,5))
                obj.get(key)
                threading._start_new_thread(__save_job51_data, (key, BeautifulSoup(obj.page_source).select('#resultList'),))
            time.sleep(5)
    except Exception as e:
        logger.error(u'下载网页数据时异常:' + e.message)
    finally:
        save_browser_open_state()
        obj.quit()
        save_browser_close_state()


################################################################################################################
def __get_news_data(key,responseBody):
    list_str = str(responseBody.find_all('div', attrs={"data-newsid": not "", "data-role": "news-item"}))
    for var in list_str.split('</div>, <div'):
        soup=BeautifulSoup(var)
        # soup = BeautifulSoup(unicode(var,'unicode-escape'))

        # 获取标题
        title = unicode.encode(soup.h4.text, 'utf-8').replace('\n', '').replace('\r', '').replace(' ', '')

        # 获取Url
        url = unicode.encode('http:' + BeautifulSoup(str(soup.h4)).a.get("href"), 'utf-8')

        # 获取发布来源
        publisher = unicode.encode(BeautifulSoup(str(soup.select('span[class="name"]'))).a.text, 'utf-8')
        # publisher = unicode(publisher, 'unicode-escape')

        #获取当前评论
        comment_count=unicode.encode(BeautifulSoup(str(soup.select('a[class="com"]'))).span.text, 'utf-8')
        # comment_count = unicode(comment_count, 'unicode-escape')

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

################################################################################################################
def __get_proxy_ip_data(key,responseBody):
    list= str(responseBody.find_all('tr','odd')).split(',')
    for var in list:
        list_str=BeautifulSoup(var).find_all('td')

        response_time = float(re.sub(u'秒', '', BeautifulSoup(str(list_str[6])).div['title']))#获取响应时间
        # response_time = float(re.sub('\\\u79d2', '', BeautifulSoup(str(list_str[6])).div['title']))  # 获取响应时间
        if response_time<1:
            ip=str(list_str[1].text) #获取代理IP
            port=str(list_str[2].text).replace('\n', '').replace('\r', '').replace(' ', '') #获取端口号
            address=BeautifulSoup(list_str[3].text).text.replace('\n', '').replace('\r', '').replace(' ', '')#获取服务器地址
            #address=unicode(str(address),'unicode-escape').replace('\n', '').replace('\r', '').replace(' ', '')
            type=str(list_str[5].text) #获取类型
            id=ip+port #生成id


            try:
                proxyIP.objects.update_or_create(id=id,ip_address=ip,ip_port=port,address=address,ip_type=type,source=key,response_time=response_time)
            except Exception as e:
                logger.error(u'保存代理Ip异常：'+e.message)

def __save_proxy_ip_data(key,responseBody):
    try:
        __get_proxy_ip_data(key,responseBody)
    except Exception as e:
        logger.error(u'抓取并保存代理IP数据异常'+e.message)

################################################################################################################

def __get_job51_data(key,responseBody):
    content = BeautifulSoup(str(responseBody)).find_all('div', 'el')
    list= str(content).split(',')
    del list[0]
    for var in list:
        soup=BeautifulSoup(var)

        job = soup.p.a
        job_name = job.get('title')
        # job_name=unicode(str(job_name),'unicode-escape')

        job_url = job.get('href')

        company = str(soup.select('span[class="t2"]'))
        company_name = BeautifulSoup(company).a.get('title')
        # company_name = unicode(str(company_name), 'unicode-escape')

        company_url = BeautifulSoup(company).a.get('href')

        job_address = BeautifulSoup(str(soup.select('span[class="t3"]'))).text.replace('[','').replace(']','')
        # job_address = unicode(str(job_address), 'unicode-escape')

        job_salary = BeautifulSoup(str(soup.select('span[class="t4"]'))).text.replace('[','').replace(']','')
        # job_salary = unicode(str(job_salary), 'unicode-escape')

        id = int(soup.input.get('value'))

        pub_date = BeautifulSoup(str(soup.select('span[class="t5"]'))).text.replace('[','').replace(']','')

        salary_temp = salary_unicode2int(job_salary)
        if salary_temp==None:
            salary_low=0
            salary_high=0
        else:
            salary_low = salary_temp.get('low')
            salary_high = salary_temp.get('high')

        try:
            job51.objects.update_or_create(id=id,job_name=job_name,job_url=job_url,company_name=company_name,company_url=company_url,
                job_address=job_address,job_salary=job_salary,pub_date=pub_date,salary_low=salary_low,salary_high=salary_high)
        except Exception as e:
            print e

def __save_job51_data(key,responseBody):
    try:
        __get_job51_data(key,responseBody)
    except Exception as e:
        logger.error(u'抓取并保存51job数据异常'+e.message)


def startCrawler():
    list_task=__get_task_list()
    if list_task is None:
        logger.info(u'本次任务结束，没有需要执行的爬虫任务')
    elif len(list_task)==0:
        logger.info(u'本次任务结束，没有需要执行的爬虫任务')
    else:
        __run(list_task)
        logger.info(u'本次爬虫任务完成')
