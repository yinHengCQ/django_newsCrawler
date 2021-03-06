from django.contrib import admin
from models import *

# Register your models here.

class newsAdmin(admin.ModelAdmin):
    list_display = ['id','title','publisher','pub_date','comment_count','url','createTime','modifyTime']
class proxyIpAdmin(admin.ModelAdmin):
    list_display = ['id','ip_address','ip_port','address','ip_type','source']
class job51Admin(admin.ModelAdmin):
    list_display = ['id','job_id','job_name','job_url','company_name','company_url','job_address','job_salary',
                    'pub_date','salary_low','salary_high','createTime','modifyTime']
class job51DetailAdmin(admin.ModelAdmin):
    list_display = ['id','job_id','job_name','company_name','company_desc','job_jtag','job_welfare','job_detail_desc',
                    'job_type_desc','job_keyword_desc','work_address','createTime','modifyTime']
class resume58Admin(admin.ModelAdmin):
    list_display = ['id','resume_id','name','sex','age','work_age','education','hope_job','now_job',
                    'hope_work_address','mark','createTime','modifyTime']
class resumeGanjiAdmin(admin.ModelAdmin):
    list_display = ['id','resume_id','name','sex','age','work_age','education','hope_job','hope_work_address','mark',
                    'hope_salary','hope_salay_low','hope_salay_high','work_type','createTime','modifyTime']

admin.site.register(news,newsAdmin)
admin.site.register(proxyIP,proxyIpAdmin)
admin.site.register(job51,job51Admin)
admin.site.register(JobDetail,job51DetailAdmin)
admin.site.register(Resume58,resume58Admin)
admin.site.register(ResumeGanji,resumeGanjiAdmin)