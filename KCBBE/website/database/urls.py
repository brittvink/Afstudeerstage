from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('title', views.titles, name="titles"),
    path('search_titles', views.search_titles, name='search-titles'),
    path('show_article/<article_id>', views.show_article, name="show-article"),

]