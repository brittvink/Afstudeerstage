from django.contrib import admin
# Register your models here.

from .models import Information, Search

admin.site.register(Information)
admin.site.register(Search)
