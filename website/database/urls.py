from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url


urlpatterns = [
    path('', views.home, name="home"),
    path('search_titles', views.search_titles_and_topics, name='search-titles'),
    path('read_rss', views.read_rss, name="read-rss"),
    path('text_field_rss/', views.text_field_rss, name="text-field-rss"),
    path('upload/', views.upload, name='upload'),
    path('api/', views.api.as_view(), name='api'),
    path('api/<article_id>', views.api.as_view(), name="api"),
    url(r'^articles/$', views.show_all_articles, name='all-articles'),
    url(r'^article/$', views.show_article, name='article' ),
    url(r'^filters/$', views.show_filters, name='all-filters'),
    url(r'^articles-of-filter/$', views.show_articles_of_filter, name='show-articles-of-filter'),
    url(r'^add_vocabulair/$', views.add_vocabulair, name="add-vocabulair"),
    url(r'^show_vocabulair/$', views.show_vocabulair, name="show-vocabulair"),
]
