#coding=utf-8
from bs4 import BeautifulSoup
from crawler.utils.dateUtil import int2date_YMDHMS
from crawler.utils.disguiseUtil import getRandomPCUserAgent,getRandomReferer
from crawler.utils.strUtil import salary_unicode2int
from crawler.models import *
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging,threading,time,re,random
from django.core.cache import cache
from crawler.service.browserService import check_browser_state,save_browser_close_state,save_browser_open_state
from lxml import etree




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
                threading._start_new_thread(__save_news_data,(key,obj.page_source,))
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
            elif task_name=='job51DetailCrawler':
                job_urls=[]
                try:job_urls=list(cache.get('job_urls'))
                except Exception as e:logger.error(u'从redis获取job_urls异常:'+str(e))
                for job_url in job_urls:
                    obj.get(job_url)
                    time.sleep(1)
                    threading._start_new_thread(__save_job_detail, (obj.page_source,))
            time.sleep(2)
    except Exception as e:
        logger.error(u'下载网页数据时异常:' + e.message)
    finally:
        save_browser_open_state()
        obj.quit()
        save_browser_close_state()


################################################################################################################
def __get_news_data(key,page):
    temp = etree.HTML(page).xpath('//div[@class="news-wrapper"]/div[@data-role="news-item"]')
    for var in temp:
        news_url = 'http:' + unicode(var.xpath('h4/a[1]/@href')[0])
        news_id = re.sub('\D', '', news_url)
        news_title = unicode(var.xpath('h4/a[1]/text()')[0].encode('unicode-escape').decode('string_escape').strip(), 'unicode-escape')
        news_publisher = unicode(var.xpath('div/span[@class="name"]/a[1]/text()')[0].encode('unicode-escape').decode('string_escape').strip(),'unicode-escape')
        comment_count = unicode(var.xpath('div/a[@class="com"]/span[1]/text()')[0])
        pub_time = unicode(var.xpath('div/span[@class="time"]/@data-val')[0])
        pub_date = int2date_YMDHMS(int(pub_time))

        try:
            orgin=news.objects.get(id=news_id)
            orgin.comment_count=comment_count
            orgin.save()
        except news.DoesNotExist:
            news.objects.create(id=news_id,title=news_title,url=news_url,publisher=news_publisher,comment_count=comment_count,pub_date=pub_date)

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
    job_urls=[]
    for var in list:
        soup=BeautifulSoup(var)

        job = soup.p.a
        job_name = job.get('title')
        # job_name=unicode(str(unicode(str(job_name), 'unicode-escape')), 'unicode-escape')

        job_url = job.get('href')
        job_urls.append(job_url)

        company = str(soup.select('span[class="t2"]'))
        company_name = BeautifulSoup(company).a.get('title')
        # company_name = unicode(str(unicode(str(unicode(str(company_name), 'unicode-escape')), 'unicode-escape')),'unicode-escape')

        company_url = BeautifulSoup(company).a.get('href')

        job_address = BeautifulSoup(str(soup.select('span[class="t3"]'))).text.replace('[','').replace(']','')
        # job_address =  unicode(str(unicode(str(unicode(str(job_address), 'unicode-escape')), 'unicode-escape')),'unicode-escape')

        job_salary = BeautifulSoup(str(soup.select('span[class="t4"]'))).text.replace('[','').replace(']','')
        # job_salary = unicode(str(unicode(str(unicode(str(job_salary), 'unicode-escape')), 'unicode-escape')),'unicode-escape')

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
            # job51.objects.update_or_create(id=id,job_name=job_name,job_url=job_url,company_name=company_name,company_url=company_url,
            #     job_address=job_address,job_salary=job_salary,pub_date=pub_date,salary_low=salary_low,salary_high=salary_high)
            try:
                orign=job51.objects.get(id=id)
                orign.job_salary=job_salary
                orign.salary_low=salary_low
                orign.salary_high=salary_high
                orign.save()
            except job51.DoesNotExist:
                job51.objects.create(id=id,job_name=job_name,job_url=job_url,company_name=company_name,company_url=company_url,
                job_address=job_address,job_salary=job_salary,pub_date=pub_date,salary_low=salary_low,salary_high=salary_high)
        except Exception as e:
            logger.error(u'保存job51异常：' + e.message+u'，当前数据id为：'+str(id)+u'，职位名称：'+job_name)
    try:
        cache.set('job_urls',job_urls)
    except Exception as e:logger.error(u'向redis中保存job_urls异常：'+str(e))

def __save_job51_data(key,responseBody):
    try:
        __get_job51_data(key,responseBody)
    except Exception as e:
        logger.error(u'抓取并保存51job数据异常：'+e.message)
##########################################################################################################################
def __save_job_detail(page):
    job_id=''
    try:
        page = page.replace('gb2312', 'utf-8')
        job_id = unicode(etree.HTML(page).xpath('//input[@id="hidJobID"]/@value')[0])
        job_name = ''
        try:job_name=unicode(etree.HTML(page).xpath('//input[@id="hidJobID"]/../@title')[0])
        except:pass
        company_name = ''
        try:company_name = unicode(etree.HTML(page).xpath('//p[@class="cname"][1]/a[1]/@title')[0])
        except:pass
        company_desc = ''
        try:company_desc = unicode(etree.HTML(page).xpath('//p[@class="msg ltype"][1]/text()')[0]).strip()
        except:pass

        job_jtag_xpath = etree.HTML(page).xpath('//div[@class="jtag inbox"][1]/div[1]/span')
        job_jtag = ''
        try:
            for var_path in job_jtag_xpath: job_jtag += (unicode(var_path.xpath('em[1]/@class')[0]) + '-' + unicode(
                var_path.xpath('text()')[0])) + ','
            job_jtag = job_jtag[:-1]
        except:pass

        job_welfare_xpath = etree.HTML(page).xpath('//div[@class="jtag inbox"][1]/p[1]/span')
        job_welfare = ''
        try:
            for var_path in job_welfare_xpath: job_welfare += unicode(var_path.xpath('text()')[0]) + ','
            job_welfare = job_welfare[:-1]
        except:pass

        job_desc_xpath = etree.HTML(page).xpath('//div[@class="bmsg job_msg inbox"][1]/*')
        job_detail_desc = ''
        try:
            for var_path in job_desc_xpath[:-3]: job_detail_desc += unicode(var_path.xpath('string(.)'))
            job_detail_desc = re.sub('\s+', '\n', job_detail_desc)
            if job_detail_desc == '':
                job_detail_desc = unicode(BeautifulSoup(page).find(name='div', attrs={'class': 'bmsg job_msg inbox'})).replace('<br/>', '^')
                job_detail_desc = unicode(etree.HTML(job_detail_desc).xpath('//div[@class="bmsg job_msg inbox"][1]/text()')[0]).strip().replace('^', '\n')
        except:pass

        job_type_desc = ''
        try:job_type_desc = re.sub('\s+', ' ', unicode(etree.HTML(page).xpath('//div[@class="mt10"][1]/p[1]')[0].xpath('string(.)'))).strip()
        except:pass

        job_keyword_desc = ''
        try:job_keyword_desc = re.sub('\s+', ' ', unicode(etree.HTML(page).xpath('//div[@class="mt10"][1]/p[2]')[0].xpath('string(.)'))).strip()
        except:pass

        work_address = ''
        try:work_address=unicode(etree.HTML(page).xpath('//div[@class="bmsg inbox"][1]/p[1]')[0].xpath('string(.)')).strip()
        except:pass

        try:
            ogrin = JobDetail.objects.get(id=job_id)
            ogrin.job_name = job_name
            ogrin.company_name = company_name
            ogrin.company_desc = company_desc
            ogrin.job_jtag = job_jtag
            ogrin.job_welfare = job_welfare
            ogrin.job_detail_desc = job_detail_desc
            ogrin.job_type_desc = job_type_desc
            ogrin.job_keyword_desc = job_keyword_desc
            ogrin.work_address = work_address
            ogrin.save()
        except JobDetail.DoesNotExist:
            JobDetail.objects.create(id=job_id, job_name=job_name, company_name=company_name, company_desc=company_desc,
                                     job_jtag=job_jtag,
                                     job_welfare=job_welfare, job_detail_desc=job_detail_desc,
                                     job_type_desc=job_type_desc,
                                     job_keyword_desc=job_keyword_desc, work_address=work_address)
        except Exception as e:
            logger.error(u'保存job51详细信息异常：' + str(e) + u',当前jobId为：' + str(job_id))
    except Exception as error:
        logger.error(u'抓取并保存51job详细数据异常：' + str(error)+ u',当前jobId为：' + str(job_id))




def startCrawler():
    list_task=__get_task_list()
    if list_task is None:
        logger.info(u'本次任务结束，没有需要执行的爬虫任务')
    elif len(list_task)==0:
        logger.info(u'本次任务结束，没有需要执行的爬虫任务')
    else:
        __run(list_task)
        logger.info(u'本次爬虫任务完成')
