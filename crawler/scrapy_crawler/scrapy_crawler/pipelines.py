# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from crawler.models import job51,JobDetail
from crawler.utils.cacheUtil import load_job51_cache,save_job51_sql_id

class ScrapyCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class Job51CrawlerPipeline(object):
    def process_item(self,item,spider):
        job_51_sql_id=load_job51_cache(item['job_id'])
        if job_51_sql_id==None:
            job_51_sql_id=job51.objects.create(job_id=item['job_id'],job_name=item['job_name'],job_url=item['job_url'],company_name=item['company_name'],company_url=item['company_url'],
                                       job_address=item['job_address'],job_salary=item['job_salary'],pub_date=item['pub_date'],salary_low=item['salary_low'],salary_high=item['salary_high']).id
            job_51_detail_sql_id=JobDetail.objects.create(job_id=item['job_id'], job_name=item['job_name'],company_name=item['company_name'],work_address=item['work_address'],
                                           company_desc=item['company_desc'],job_jtag=item['job_jtag'],job_welfare=item['job_welfare'],job_detail_desc=item['job_detail_desc'],
                                           job_type_desc=item['job_type_desc'],job_keyword_desc=item['job_keyword_desc']).id
            save_job51_sql_id(item['job_id'],'{0},{1}'.format(job_51_sql_id,job_51_detail_sql_id))
        else:
            job_51_sql_id=job_51_sql_id.split(',')
            job51.objects.update(id=job_51_sql_id[0],job_name=item['job_name'],job_url=item['job_url'],company_name=item['company_name'],company_url=item['company_url'],
                                       job_address=item['job_address'],job_salary=item['job_salary'],pub_date=item['pub_date'],salary_low=item['salary_low'],salary_high=item['salary_high'])
            JobDetail.objects.update(id=job_51_sql_id[1], job_name=item['job_name'],company_name=item['company_name'],work_address=item['work_address'],
                                           company_desc=item['company_desc'],job_jtag=item['job_jtag'],job_welfare=item['job_welfare'],job_detail_desc=item['job_detail_desc'],
                                           job_type_desc=item['job_type_desc'],job_keyword_desc=item['job_keyword_desc'])
        return item
