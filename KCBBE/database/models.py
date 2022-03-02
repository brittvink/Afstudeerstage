from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Information(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=100)
    summary = models.CharField(max_length=1000)
    published = models.CharField(max_length = 100)

    def __str__(self):
        return self.title

class Search(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    key_id = models.CharField(max_length=100)
    article_id = models.CharField(max_length=100)

    def __str__(self):
        return self.id

class Search_info(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    searched_title = models.CharField(max_length=100)
    searched_topic = models.CharField(max_length=100)

# - Keyword id
# - artikel id
# - hoe vaak is het woord gevonden (optional)
#
# key
# - inforamtie over het keyword


