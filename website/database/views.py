from .models import Information, Search, Vocabulair

from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404

from .lezen_van_rss import main
from .stoppen_in_database import main_stoppen
from .serializers import InformationSerializers
from .make_json import jsonmain
from .add_word_to_vocabulaire_db import add_word_to_db
from .webscraping import main_webscraping
from .make_filter import main_make_filter

import os
import urllib

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
            'search_titles.html',
            {'searched': searched_dict, 'articles': articles})

    else:
        return render(request, 'search.html', {})


def read_rss(request):
    """
    This function redirect to either a page to upload a textfile or fill in a text field,
    both to add data to the db
    """
    if request.method == "POST":
        if request.POST.get('action') == "fill_txt_field":
            return redirect('text-field-rss')
        else:
            return redirect('upload/')

    return render(request, 'upload_data_to_db/read_rss.html')


def text_field_rss(request):
    """
    If the text field is filled, the link will be paresed to be read and put in the database
    """
    context = {}
    if request.method == "POST":
        rss = request.POST['rss']

        returnvalue = main(rss)

        # If the link is valid and data is put in a text file, the file can be put in the db
        if returnvalue == "Er is data opgehaald van de link":
            main_stoppen()

        context['return_value'] = returnvalue

    return render(request, 'upload_data_to_db/text_field_rss.html', context)


def upload(request):
    """
    If a file is uploaded, the links are read and data is put in the database
    """
    context = {}

    if request.method == 'POST':
        # Save uploaded file
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

        cwd = os.getcwd()
        new_added_file = os.path.join(cwd + fs.url(name))

        # Read all lines in file
        with open(new_added_file) as f:
            lines = f.readlines()

        # Add rss link by link
        for line in lines:
            line = line.strip()
            # Read rss link
            returnvalue = main(line)

            # If the link is valid and data is put in a text file, the file can be put in the db
            if returnvalue == "Er is data opgehaald van de link":
                main_stoppen()

        context['return_value'] = returnvalue

    return render(request, 'upload_data_to_db/upload.html', context)


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


def show_filters(request):
    """
    Show all filters
    """
    all_filters = Search.objects.all()
    topics_list = []

    for filter in all_filters:
        if filter.search_id not in topics_list:
            topics_list.append(filter.search_id)
    return render(request, 'showfilter.html', {'topics_list': topics_list})


def show_articles_of_filter(request):
    """
    Show all articles that are found using a filter
    """
    filter_ids = request.GET.getlist('item')
    and_or = request.GET.get('type')

    all_lists_with_articles = []

    for filter_id in filter_ids:

        # Use sql query code to find the articles that match the filter ID
        articles = Information.objects.raw(
                """select KCBBE2.database_Information.id 
                from KCBBE2.database_Information 
                inner join KCBBE2.database_Search 
                on KCBBE2.database_Information.id=KCBBE2.database_Search.article_id 
                where KCBBE2.database_Search.search_id = '"""
                + filter_id + """'""")

        # Articles of all filterid will be added to a list
        all_lists_with_articles.append(articles)

    # If the articles should have multiple filters, only the articles that are found for all filters should be returned
    if and_or == 'and':
        filtered_set = set.intersection(*[set(x) for x in all_lists_with_articles])
        # Make list of a set
        list_with_articles_to_return =  (list(filtered_set))

    # Else return all articles, make one list of the multiple lists
    else:
        list_with_articles_to_return = [item for sublist in all_lists_with_articles for item in sublist]

    return render(request, 'show_all_articles_of_filter.html', {'articles_list': list_with_articles_to_return})


def add_vocabulair(request):
    """
    Add a word to the Vocabulaire table in the database
    """

    key = request.GET.get('key')
    if key == None:
        key = ""

    if request.method == "POST":
        parent = request.POST['onder']
        child = request.POST['woord']

        add_word_to_db(parent, child)

        return render(request, 'vocabulair.html', {'onder': parent, 'woord': child})
    else:
        return render(request, 'vocabulair.html', {'key': key })


def show_vocabulair(request):
    all_synonymes = Vocabulair.objects.all()

    list_with_all_different_synonymes = {}

    for synonyme in all_synonymes:
        if synonyme.key_id not in list_with_all_different_synonymes:
            list_with_all_different_synonymes[synonyme.key_id] = []
        list_with_all_different_synonymes[synonyme.key_id].append(synonyme)

    return render(request, 'show_vocabulair.html', {"list_different_synonymes": list_with_all_different_synonymes})

def make_text_files(request):
    all_articles = Information.objects.all()
    for article in all_articles:
        print(article.id)

        result = main_webscraping(article.link)
        filename = "media/articles/" + article.id + ".txt"
        f = open(filename, "w")
        f.write(result)
        f.close()

def make_filter(request):

    if request.method == "POST":
        input = request.POST['filter']
        all_articles = Information.objects.all()

        main_make_filter(input, all_articles)
        return redirect('all-filters')

    return render(request, 'make_filter.html')