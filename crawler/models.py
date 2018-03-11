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

class proxyIP(models.Model):
    id=models.CharField(primary_key=True,max_length=25)
    ip_address=models.CharField(max_length=20)
    ip_port=models.IntegerField()
    address=models.CharField(max_length=10)
    ip_type=models.CharField(max_length=5)
    source = models.CharField(max_length=30)
    response_time=models.FloatField()
    createTime=models.DateTimeField(auto_now_add=True)
    modifyTime=models.DateTimeField(auto_now=True)

class job51(models.Model):
    job_id=models.IntegerField()
    job_name=models.CharField(max_length=100)
    job_url=models.CharField(max_length=300)
    company_name=models.CharField(max_length=60)
    company_url=models.CharField(max_length=300)
    job_address=models.CharField(max_length=20)
    job_salary=models.CharField(max_length=20)
    pub_date=models.CharField(max_length=10)
    salary_low=models.IntegerField()
    salary_high=models.IntegerField()
    createTime=models.DateTimeField(auto_now_add=True,null=True)
    modifyTime=models.DateTimeField(auto_now=True)


class JobDetail(models.Model):
    job_id=models.IntegerField()
    job_name=models.CharField(max_length=100)
    company_name=models.CharField(max_length=60)
    company_desc=models.CharField(max_length=200)
    job_jtag=models.CharField(max_length=300)
    job_welfare=models.CharField(max_length=300)
    job_detail_desc=models.CharField(max_length=5000)
    job_type_desc=models.CharField(max_length=300)
    job_keyword_desc = models.CharField(max_length=300)
    work_address=models.CharField(max_length=200)
    createTime=models.DateTimeField(auto_now_add=True,null=True)
    modifyTime=models.DateTimeField(auto_now=True)