from hashlib import md5
from django.db import models


# Create your models here.


class Paste(models.Model):
    key = models.CharField(max_length=40, unique=True, null=False)
    content = models.TextField(default='')


class PasteAnalytic(models.Model):
    paste = models.ForeignKey(Paste, on_delete=models.CASCADE)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


