from .models import Articles
from django.db.models import Q
from django.shortcuts import render
from .serializers import InformationSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import pickle

# from website.get_articles_with_distance import *

# Create your views here.
def home(request):
    """
    Shows home page
    """
    return render(request, 'home.html')
    # return render(request, 'graph.html')


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
        articles = Articles.objects.filter(query).order_by('title')

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
            articles = Articles.objects.all()
            serializer = InformationSerializers(articles, many=True)
            return Response(serializer.data)
        # If ID is parsed, only that information will be shown
        else:
            articles = Articles.objects.filter(id = article_id)
            serializer = InformationSerializers(articles, many=True)
            return Response(serializer.data)


def show_all_articles(request):
    """
    Show all articles
    """
    # make_text_files(request)
    article_list = Articles.objects.all().order_by('title')
    return render(request, 'show_all_articles.html', {'article_list': article_list})


def show_article(request):
    """
    Show article with details
    """
    query = request.GET.get('item')
    article = Articles.objects.get(title=query)

    filename = "media/articles/" + article.id + ".txt"
    f = open(filename, "r")
    result = f.readlines()
    f.close()
    result = result[0]

    return render(request, 'showing_articles/show_article.html', {'article': article, 'article_text': result})

def related(request):
    all_articles = Articles.objects.all()
    all_articles_list = []
    for article in all_articles:
        all_articles_list.append(article.title)

    if request.method == "POST":

        # Make variable of filled in text in form
        searched_title = request.POST['searched']
        type = request.POST['type']
        min_sim = request.POST['min_similarity']
        max_articles = request.POST['max_articles']
        if min_sim == "No":
            min_sim = 5

        find_articles(searched_title, type, min_sim, max_articles)

        return render(request, 'related_graph.html')

    return render(request, 'related.html', {'articles' : sorted(all_articles_list)})


def find_articles(searched_title, type, min_sim, max_articles):
    if type == "Word2Vec":
        with open('df_article_distance_tokenized_data.pkl', 'rb') as handle:
            dictionary_distance = pickle.load(handle)
    else:
        with open('tf-idf_cleaned_text.pkl', 'rb') as handle:
            dictionary_distance = pickle.load(handle)

    article = Articles.objects.get(title=searched_title)

    return_dict = {}
    for article, similarity in [(article, 0)]:
        return_dict["name"] = article.title
        return_dict["linkje"] = "article/?item=" + article.title
        return_dict["children"] = []
        new_dict = dict(sorted(dictionary_distance.get(article.id).items(), key=lambda item: item[1]))
        for article_child, similarity_child in list(new_dict.items())[1: int(max_articles) + 1]:
            if similarity_child < float(min_sim):
                article_child = Articles.objects.get(id=article_child)
                return_dict["children"].append({"name": article_child.title, "similarity":similarity_child, "linkje":"article?item=" + article_child.title})


    list_children = []
    for i in return_dict["children"]:
        list_children.append((i["name"], i["similarity"]))


    for article, sim in list_children:
        article = Articles.objects.get(title=article)
        for child in return_dict["children"]:
            if child["name"] == article.title:
                child["link"] = "article/?item" + article.title
                child["children"] = []
                new_dict = dict(sorted(dictionary_distance.get(article.id).items(), key=lambda item: item[1]))
                for article_child, similarity_child in list(new_dict.items())[1: int(max_articles) + 1]:
                    if similarity_child < float(min_sim):
                        article_child = Articles.objects.get(id=article_child)
                        child["children"].append({"name": article_child.title, "similarity":similarity_child, "linkje":"article?item=" + article_child.title})


    with open("media/json_data.json", "w") as outfile:
        json.dump(return_dict, outfile)