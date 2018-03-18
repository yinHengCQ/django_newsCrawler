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


admin.site.register(news,newsAdmin)
admin.site.register(proxyIP,proxyIpAdmin)
admin.site.register(job51,job51Admin)
admin.site.register(JobDetail,job51DetailAdmin)
