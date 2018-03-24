# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from crawler.models import job51,JobDetail
import scrapy

class ScrapyCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class Job51CrawlerPipeline(object):
    def process_item(self,item,spider):
        job51.objects.create(job_id=item['job_id'],job_name=item['job_name'],job_url=item['job_url'],company_name=item['company_name'],company_url=item['company_url'],
                                   job_address=item['job_address'],job_salary=item['job_salary'],pub_date=item['pub_date'],salary_low=item['salary_low'],salary_high=item['salary_high'])
        JobDetail.objects.create(job_id=item['job_id'], job_name=item['job_name'],company_name=item['company_name'],work_address=item['work_address'],
                                       company_desc=item['company_desc'],job_jtag=item['job_jtag'],job_welfare=item['job_welfare'],job_detail_desc=item['job_detail_desc'],
                                       job_type_desc=item['job_type_desc'],job_keyword_desc=item['job_keyword_desc'])
        return item


# class Resume58CrawlerPipeline(object):
#     def get_media_requests(self, item, info):
#         for image_url in item['photo_url']:
#             print(image_url)
#             yield scrapy.Request(image_url)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]      # ok判断是否下载成功
#         #item['image_paths'] = image_paths
#         return item