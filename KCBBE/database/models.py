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
    searched_titles = models.CharField(max_length=100)
    searched_topics = models.CharField(max_length=100)
    number_found_articles = models.IntegerField()

    def __str__(self):
        return self.id

class Article_search(models.Model):
    found_articles = models.ForeignKey(
        Information, on_delete=models.CASCADE)
    search_details = models.ForeignKey(
        Search, on_delete=models.CASCADE)


