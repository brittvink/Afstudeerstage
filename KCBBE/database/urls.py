from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url


urlpatterns = [
    path('', views.home, name="home"),
    path('title', views.titles, name="titles"),
    path('search_titles', views.search_titles, name='search-titles'),
    path('show_article/<article_id>', views.show_article, name="show-article"),
    path('read_rss', views.read_rss, name="read-rss"),
    path('text_field_rss/', views.text_field_rss, name="text-field-rss"),
    path('upload/', views.upload, name='upload'),
    path('api/', views.api.as_view(), name='api'),
    path('api/<article_id>', views.api.as_view(), name="api"),
    path('show_all_filters', views.show_all_filters, name='show-all-filters'),
    path('show_filter_articles/<filter_id>', views.show_articles_with_this_filter_id, name='show-filter-articles'),
    path('plaatje', views.graph, name='plaatje'),
    url(r'^search/$', views.search, name='search_view'),
    url(r'^search2/$', views.search2, name='search_view2'),
    url(r'^hoi/$', views.hoi, name='hoi2'),
    url(r'^filter/$', views.filter, name='filter22' ),
    url(r'^filters/$', views.hoi3, name='hoi3'),
    url(r'^filter-now/$', views.filter222, name='show-filter-22'),

]
