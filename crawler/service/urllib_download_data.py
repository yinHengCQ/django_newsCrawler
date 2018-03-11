#coding=utf-8
import urllib2,time,re,logging
from lxml import etree
from crawler.models import job51,JobDetail
from crawler.utils.strUtil import salary_unicode2int
from bs4 import BeautifulSoup
from crawler.utils.disguiseUtil import getRandomPCUserAgent
from django.core.cache import cache


__logger=logging.getLogger('django')

def __get_page_index():
    try:
        page = cache.get('job51Crawler_page')
        if page==None:page=1;cache.set('job51Crawler_page','1');
        elif page=='2000':cache.set('job51Crawler_page','1')
        else:cache.set('job51Crawler_page',str(int(page)+1))
        return page
    except Exception as e:__logger.error(u'获取页面失败');raise e

def download_51job():
    start_time=time.time()
    page_index=__get_page_index()
    __logger.info(u'开始51job爬虫任务,当前页面为：{0}'.format(page_index))
    try:
        url = "http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,{0}.html".format(page_index)
        headers = {"User-Agent": getRandomPCUserAgent()}
        request = urllib2.Request(url=url, headers=headers)
        job_url_list=__save_job_desc(urllib2.urlopen(request).read())

        for var in job_url_list:
            __save_job_detail(urllib2.urlopen(urllib2.Request(url=var, headers=headers)).read())

    except Exception as e:__logger.error(u'爬取51job任务异常：{0}'.format(e))
    finally:__logger.info(u'本次51job任务完成，耗时{0}'.format(time.time()-start_time))

def __save_job_desc(page):
    base_xpath = etree.HTML(page).xpath('//div[@id="resultList"]/div[@class="el"]')
    job_url_list=[]
    for var in base_xpath:
        job_name=''
        try:
            job_id = var.xpath('p[1]/input[1]/@value')[0]
            job_name = var.xpath('p[1]/span[1]/a[1]/@title')[0]
            job_url = var.xpath('p[1]/span[1]/a[1]/@href')[0]
            job_url_list.append(job_url)
            company_name = var.xpath('span[@class="t2"][1]/a[1]/@title')[0]
            company_url = var.xpath('span[@class="t2"][1]/a[1]/@href')[0]
            job_address = var.xpath('span[@class="t3"][1]/text()')[0]
            job_salary = var.xpath('span[@class="t4"][1]/text()')[0]
            pub_date = var.xpath('span[@class="t5"][1]/text()')[0]
            salary_temp = salary_unicode2int(job_salary)
            if salary_temp == None:salary_low = 0;salary_high = 0
            else:salary_low = salary_temp.get('low');salary_high = salary_temp.get('high')
        except Exception as error:__logger.error(u'获取51job信息异常：{0}，当前名称为：{1}'.format(error, job_name));continue
        try:
            job51.objects.update_or_create(job_id=job_id, job_name=job_name.encode('utf-8'), job_url=job_url,company_name=company_name.encode('utf-8'), company_url=company_url,
                                           job_address=job_address.encode('utf-8'),job_salary=job_salary.encode('utf-8'), pub_date=pub_date,salary_low=salary_low, salary_high=salary_high)
        except Exception as e:__logger.error(u'保存51job信息异常：{0}，当前名称为：{1}'.format(e, job_name))

    return job_url_list

def __get_str_from_tag(page,begin_tag,end_tag,block_str):
    begin=page.find(begin_tag)
    end=page[begin:].find(end_tag)
    return re.sub('\s+','',page[begin:][:end].replace(begin_tag, '').strip().replace(block_str,''))

def __save_job_detail(page):
    base_xpath=etree.HTML(page)
    job_name=''
    try:
        job_id = base_xpath.xpath('//input[@id="hidJobID"]/@value')[0]
        job_name = unicode(base_xpath.xpath('//input[@id="hidJobID"]/../@title')[0])
        company_name = unicode(base_xpath.xpath('//p[@class="cname"][1]/a[1]/@title')[0])
        company_desc = __get_str_from_tag(page, '<p class="msg ltype">', '</p>', '&nbsp;').decode('gbk')
    except Exception as e:__logger.error(u'获取51job详情异常：{0}，当前名称为：{1}'.format(e,job_name));return

    job_jtag_xpath = base_xpath.xpath('//div[@class="jtag inbox"][1]/div[1]/span')
    job_jtag = u''
    try:
        for var_path in job_jtag_xpath: job_jtag += '{0}:{1},'.format(var_path.xpath('em[1]/@class')[0],__get_str_from_tag(page,'<em class="{0}"></em>'.format(var_path.xpath('em[1]/@class')[0]),'</span>', '')).decode('gbk')
        job_jtag = job_jtag[:-1]
    except:pass

    job_welfare = u''
    try:job_welfare=__get_str_from_tag(page,'<p class="t2">','</p>','').replace('</span><span>',',').replace('<span>','').replace('</span>','').decode('gbk')
    except:pass

    job_desc_xpath = base_xpath.xpath('//div[@class="bmsg job_msg inbox"][1]/*')
    job_detail_desc = u''
    try:
        for var_path in job_desc_xpath[:-3]: job_detail_desc += unicode(var_path.xpath('string(.)'))
        job_detail_desc = re.sub('\s+', '\n', job_detail_desc)
        if job_detail_desc == '':
            job_detail_desc = BeautifulSoup(page).find(name='div', attrs={'class': 'bmsg job_msg inbox'}).replace('<br/>', '^')
            job_detail_desc = etree.HTML(job_detail_desc).xpath('//div[@class="bmsg job_msg inbox"][1]/text()')[0].strip().replace('^', '\n')
    except:pass

    job_type_desc = u''
    try:job_type_desc = re.sub('\s+', ' ', base_xpath.xpath('//div[@class="mt10"][1]/p[1]')[0].xpath('string(.)')).strip()
    except:pass

    job_keyword_desc = u''
    try:job_keyword_desc=__get_str_from_tag(page,'<p class="fp">','</p>','').replace('</span><spanclass="el">',',</span><spanclass="el">').replace('<spanclass="label">','').replace('</span>','').replace('<spanclass="el">','').replace('：,',',').decode('gbk')
    except:pass

    work_address = u''
    try:work_address = base_xpath.xpath('//div[@class="bmsg inbox"][1]/p[1]')[0].xpath('string(.)').strip()
    except:pass

    try:JobDetail.objects.update_or_create(job_id=job_id,job_name=job_name,company_name=company_name,company_desc=company_desc,job_jtag=job_jtag,job_welfare=job_welfare,
                                           job_detail_desc=job_detail_desc,job_type_desc=job_type_desc,job_keyword_desc=job_keyword_desc,work_address=work_address)
    except Exception as error:__logger.error(u'保存51job详情异常：{0}，当前名称为：{1}'.format(error, job_name))



