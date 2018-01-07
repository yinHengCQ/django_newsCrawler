#coding=utf-8
from django.test import TestCase

# Create your tests here.

# def salary_str2int(salary):
#     # list_temp=salary.replace('千','').replace('月','').replace('万','').replace('年','').replace('/','').split('-')
#     list_temp = salary.replace('千'.decode('utf-8'), '').replace('月'.decode('utf-8'), '').replace('万'.decode('utf-8'), '').replace('年'.decode('utf-8'), '').replace('/', '').split('-')
#     if salary.find('月'.decode('utf-8'))>0:
#         if salary.find('千'.decode('utf-8'))>0:
#             low=int(float(list_temp[0])*1000)
#             high=int(float(list_temp[1])*1000)
#         elif salary.find('万'.decode('utf-8'))>0:
#             low = int(float(list_temp[0]) * 10000)
#             high = int(float(list_temp[1]) * 10000)
#         return {'low':low,'high':high}
#     elif salary.find('年'.decode('utf-8'))>0:
#         low = int(float(list_temp[0]) * 10000)/12
#         high = int(float(list_temp[1]) * 10000)/12
#         return {'low':low,'high':high}
#
# a=unicode('1111')
# print a
# print type(a)
# print int(a)


from bs4 import BeautifulSoup
# f='<div class="el"><p class="t1 "><em class="check" name="delivery_em" onclick="checkboxClick(this)"></em><input class="checkbox" jt="0" name="delivery_jobid" style="display:none" type="checkbox" value="93736092"><span><a href="http://jobs.51job.com/chongqing/93736092.html?s=01&amp;t=0" onmousedown="" target="_blank" title="销售经理">销售经理                                </a></span></input></p><span class="t2"><a href="http://jobs.51job.com/all/co3465561.html" target="_blank" title="重庆娜笛服饰有限公司">重庆娜笛服饰有限公司</a></span><span class="t3">重庆</span><span class="t4">6-8千/月</span><span class="t5">01-06</span></div>'
#
# soup=BeautifulSoup(f)
#
# job=soup.p.a
# job_name = job.get('title')
# job_url = job.get('href')
# company=str(soup.select('span[class="t2"]'))
# company_name = BeautifulSoup(company).a.get('title')
# company_url = BeautifulSoup(company).a.get('href')
# job_address = BeautifulSoup(str(soup.select('span[class="t3"]'))).text.replace('[','').replace(']','')
# job_salary = BeautifulSoup(str(soup.select('span[class="t4"]'))).text.replace('[','').replace(']','')
# id = int(soup.input.get('value'))
# pub_date = BeautifulSoup(str(soup.select('span[class="t5"]'))).text.replace('[','').replace(']','')
#
# print job_name
# print job_url
# print company_name
# print company_url
# print job_address
# print job_salary
# print id
# print pub_date

b='1'
a='http://search.51job.com/list/060000,000000,0000,00,9,99,%2B,2,'+b+'.html'
print a
