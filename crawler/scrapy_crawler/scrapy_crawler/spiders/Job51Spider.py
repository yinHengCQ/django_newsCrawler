#coding=utf-8
import scrapy,re,logging
from scrapy.selector import Selector
from crawler.scrapy_crawler.scrapy_crawler.items import Job51CrawlerItem
from crawler.utils.strUtil import salary_unicode2int
from scrapy import log
from crawler.utils.cacheUtil import is_job_id_exists



def __get_str_from_tag(page,begin_tag,end_tag,block_str):
    begin=page.find(begin_tag)
    end=page[begin:].find(end_tag)
    return re.sub('\s+','',page[begin:][:end].replace(begin_tag, '').strip().replace(block_str,''))

class Job51Spider(scrapy.Spider):
    name = "job51_crawler"
    url_template="http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,{0}.html"
    start_urls=[]
    for var in range(1,2):
        start_urls.append(url_template.format(var))

    def parse(self, response):
        site=Selector(response)
        base_xpath = site.xpath('//div[@id="resultList"]/div[@class="el"]')
        detail_urls=[]
        log.msg("current page is {0}".format(response.url), level=log.INFO)

        for var in base_xpath:
            try:
                item = Job51CrawlerItem()
                item['job_id'] = var.xpath('p[1]/input[1]/@value').extract()[0]
                # if is_job_id_exists(item['job_id']):continue

                item['job_name'] = var.xpath('p[1]/span[1]/a[1]/@title').extract()[0]
                item['job_url'] = var.xpath('p[1]/span[1]/a[1]/@href').extract()[0]
                detail_urls.append(item['job_url'])
                item['company_name'] = var.xpath('span[@class="t2"][1]/a[1]/@title').extract()[0]
                item['company_url'] = var.xpath('span[@class="t2"][1]/a[1]/@href').extract()[0]
                try:item['job_address'] = var.xpath('span[@class="t3"][1]/text()').extract()[0]
                except:item['job_address'] = ''
                try:item['job_salary'] = var.xpath('span[@class="t4"][1]/text()').extract()[0]
                except:item['job_salary'] = ''
                item['pub_date'] = var.xpath('span[@class="t5"][1]/text()').extract()[0]
                salary_temp = salary_unicode2int(item['job_salary'])
                if salary_temp == None:salary_low = 0;salary_high = 0
                else:salary_low = salary_temp.get('low');salary_high = salary_temp.get('high')
                item['salary_low'] = salary_low
                item['salary_high'] = salary_high
                yield scrapy.Request(item['job_url'], meta={'item': item}, callback=self.parse_detail)
            except:pass


    def parse_detail(self, response):
        site = Selector(response)
        item=response.meta['item']

        try:item['work_address'] = site.xpath('//div[@class="bmsg inbox"][1]/p[1]')[0].xpath('string(.)').extract()[0].strip()
        except:item['work_address']=''
        try:item['company_desc']=site.xpath('//p[@class="msg ltype"][1]/text()').extract()[0].strip()
        except:item['company_desc']=''
        try:item['job_jtag']=''.join((var.xpath('text()').extract()[0]+"|") for var in site.xpath('//span[@class="sp4"]'))[:-1]
        except:item['job_jtag']=''
        try:item['job_welfare']=''.join((var.xpath('text()').extract()[0]+"|") for var in site.xpath('//p[@class="t2"]/span'))[:-1]
        except:item['job_welfare']=''
        try:
            temp = site.xpath('//div[@class="bmsg job_msg inbox"][1]')[0].xpath('string(.)').extract()[0].strip()
            item['job_detail_desc'] = temp[:temp.find(u'职能类别：')].strip()
        except:item['job_detail_desc']=''
        try:item['job_type_desc']=''.join((var.xpath('text()').extract()[0]+'|') for var in site.xpath('//div[@class="mt10"][1]/p[@class="fp"][1]/span[@class="el"]'))
        except:item['job_type_desc']=''
        try:item['job_keyword_desc']=''.join((var.xpath('text()').extract()[0]+'|') for var in site.xpath('//div[@class="mt10"][1]/p[@class="fp"][2]/span[@class="el"]'))
        except:item['job_keyword_desc']=''

        yield item