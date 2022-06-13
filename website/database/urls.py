from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include, re_path


urlpatterns = [
    path('', views.home, name="home"),
    path('search_titles', views.search_titles_and_topics, name='search-titles'),
    path('api/', views.api.as_view(), name='api'),
    path('api/<article_id>', views.api.as_view(), name="api"),
    re_path(r'^articles/$', views.show_all_articles, name='all-articles'),
    re_path(r'^article/$', views.show_article, name='article' ),
    path('related', views.related, name='related')
]
