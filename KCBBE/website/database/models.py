from django.db import models


# Create your models here.
class Information(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    published = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

