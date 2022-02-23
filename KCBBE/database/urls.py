from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('title', views.titles, name="titles"),
    path('search_titles', views.search_titles, name='search-titles'),
    path('show_article/<article_id>', views.show_article, name="show-article"),
    path('read_rss', views.read_rss, name="read-rss"),
    path('text_field_rss', views.text_field_rss, name="text-field-rss"),
    path('upload/', views.upload, name='upload'),
]
