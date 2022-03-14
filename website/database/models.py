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
    search_id = models.CharField(max_length=100)
    article_id = models.CharField(max_length=100)

    def __str__(self):
        return self.id

class Vocabulair(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    key_id = models.CharField(max_length=100)
    word = models.CharField(max_length=100)

#vierlettercode, zelfde lengte
#tag tag value waarden



# Andere manier van zoeken, niet via wb, gecontroleerde vocablulaire,
# zoeken met een begrip ipv losse woorden, radpeseed(olieen, plantenolie), wij zelf bedenken, db waar we die woorden verzamelen
# twee unique, identifier concdpt id, naam hebben
# Begin met olien
# resultaten laten zien afhankelijk filter, filterid
# Check met 'normale search'

