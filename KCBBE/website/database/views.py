from django.shortcuts import render
from .models import Information
from django.db import connection
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request, 'home.html')


def titles(request):
    title_list = Information.objects.all()
    return render(request, 'title_list.html', {'title_list': title_list})


def search_titles(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched_topic = request.POST['searched-topic']
        searched_topic = searched_topic.split(' ')
        query = Q()

        for topic in searched_topic:
            query = query & Q(summary__icontains=topic)

        query = query & Q(title__icontains=searched)
        print(query)
        titles2 = Information.objects.filter(query)
        return render(request,
            'search_titles.html',
            {'searched2': searched_topic, 'articles2': titles2})

    else:
        return render(request, 'search_titles.html', {})


def show_article(request, article_id):
    article = Information.objects.get(pk=article_id)
    return render(request, 'show_article.html', {'article': article})