from django.db import models

# Create your models here.
class news(models.Model):
    title=models.CharField(max_length=1024)
    publisher=models.CharField(max_length=1024)
    pub_date=models.CharField(max_length=1024)
    comment_count=models.IntegerField
    url=models.CharField(max_length=1024)

    def __str__(self):
        return self.title