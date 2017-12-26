from django.db import models

# Create your models here.
class news(models.Model):
    id=models.CharField(primary_key=True,max_length=30)
    title=models.CharField(max_length=1024)
    publisher=models.CharField(max_length=1024)
    pub_date=models.CharField(max_length=1024)
    comment_count=models.CharField(max_length=32,default='0')
    url=models.CharField(max_length=1024)

    def __str__(self):
        return self.title