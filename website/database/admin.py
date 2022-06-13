from django.contrib import admin
# Register your models here.

from .models import Articles, Search

admin.site.register(Articles)
admin.site.register(Search)
