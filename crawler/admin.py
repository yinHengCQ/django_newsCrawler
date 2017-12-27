from django.contrib import admin
from models import *

# Register your models here.

class newsAdmin(admin.ModelAdmin):
    list_display = ['id','title','publisher','pub_date','comment_count','url','createTime','modifyTime']


admin.site.register(news,newsAdmin)
