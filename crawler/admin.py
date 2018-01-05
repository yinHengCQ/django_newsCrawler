from django.contrib import admin
from models import *

# Register your models here.

class newsAdmin(admin.ModelAdmin):
    list_display = ['id','title','publisher','pub_date','comment_count','url','createTime','modifyTime']
class proxyIpAdmin(admin.ModelAdmin):
    list_display = ['id','ip_address','ip_port','address','ip_type','source']


admin.site.register(news,newsAdmin)
admin.site.register(proxyIP,proxyIpAdmin)