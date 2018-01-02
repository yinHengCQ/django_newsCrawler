from django.db import models

# Create your models here.
class news(models.Model):
    id=models.CharField(primary_key=True,max_length=30)
    title=models.CharField(max_length=1024)
    publisher=models.CharField(max_length=1024)
    pub_date=models.CharField(max_length=1024)
    comment_count=models.CharField(max_length=32,default='0')
    url=models.CharField(max_length=1024)
    createTime=models.DateTimeField(auto_now_add=True)
    modifyTime=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class browserRecord(models.Model):
    key=models.CharField(primary_key=True,max_length=255)
    status=models.BooleanField(default=False)
    totleFail=models.IntegerField()

class proxyIP(models.Model):
    ip_address=models.CharField(max_length=20)
    ip_port=models.IntegerField()
    address=models.CharField(max_length=10)
    ip_type=models.CharField(max_length=5)
    source=models.CharField(max_length=30)



# class crawlerManager(models.Model):
#     targetUrl=models.CharField(max_length=1024)