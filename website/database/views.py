from .models import Information
from django.db.models import Q
from django.shortcuts import render
from .serializers import InformationSerializers
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def home(request):
    """
    Shows home page
    """
    return render(request, 'graph.html')


def search_titles_and_topics(request):
    """
    If the seach fields are filled, the models are searched for articles that meet the criteria
    """
    # If search fields are filled in and commited
    if request.method == "POST":
        # Make variable of filled in text in form
        searched_title = request.POST['searched']
        searched_topic = request.POST['searched-topic']
        searched_topic = searched_topic.split(' ')
        searched_title = searched_title.split(' ')
        searched_dict = {"title": searched_title, "summary": searched_topic}

        # Create seach query to find articles that match
        query = Q()

        for topic in searched_topic:
            query = query & Q(summary__icontains=topic)

        for word in searched_title:
            query = query & Q(title__icontains=word)

        # find articles that match searched words
        articles = Information.objects.filter(query).order_by('title')

        # Return
        return render(request,
            'found_searched_articles.html',
            {'searched': searched_dict, 'articles': articles})

    else:
        return render(request, 'search_for_articles.html', {})


class api(APIView):
    """
    API is available, if an article id is parsed, only that information in available
    """
    def get(self, request, article_id = all):
        # If no specific ID is parsed, all information will be showed
        if article_id == all:
            articles = Information.objects.all()
            serializer = InformationSerializers(articles, many=True)
            return Response(serializer.data)
        # If ID is parsed, only that information will be shown
        else:
            articles = Information.objects.filter(id = article_id)
            serializer = InformationSerializers(articles, many=True)
            return Response(serializer.data)


def show_all_articles(request):
    """
    Show all articles
    """
    # make_text_files(request)
    article_list = Information.objects.all().order_by('title')
    return render(request, 'show_all_articles.html', {'article_list': article_list})


def show_article(request):
    """
    Show article with details
    """
    query = request.GET.get('item')
    article = Information.objects.get(title=query)

    filename = "media/articles/" + article.id + ".txt"
    f = open(filename, "r")
    result = f.readlines()
    f.close()
    result = result[0]

    return render(request, 'showing_articles/show_article.html', {'article': article, 'article_text': result})

