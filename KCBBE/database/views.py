from .models import Information, Search

from django.db import connection
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404

from .lezen_van_rss import main
from .stoppen_in_database import main_stoppen
from .serializers import InformationSerializers

import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.
def home(request):
    """
    Shows home page
    """
    return render(request, 'home.html')


def titles(request):
    """
    Shows all titles in models.Information
    """
    title_list = Information.objects.all().order_by('title')
    return render(request, 'showing_articles/title_list.html', {'title_list': title_list})


def search_titles(request):
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
        titles = Information.objects.filter(query).order_by('title')

        # Return
        return render(request,
            'search_titles.html',
            {'searched': searched_dict, 'articles': titles})

    else:
        return render(request, 'search_titles.html', {})


def show_article(request, article_id):
    """
    Shows article with the matching article id
    """
    article = Information.objects.get(pk=article_id)
    return render(request, 'showing_articles/show_article.html', {'article': article})


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
        old_number_of_articles_in_db = Information.objects.all()

        returnvalue = main(rss)
        # If the link is valid and data is put in a text file, the file can be put in the db
        if returnvalue == "Er is data opgehaald van de link":
            main_stoppen()

        new_number_of_articles_in_db = Information.objects.all()

        toegevoegd = len(new_number_of_articles_in_db) - len(old_number_of_articles_in_db)
        context['added_to_db'] = toegevoegd
        context['return_value'] = returnvalue

    return render(request, 'upload_data_to_db/text_field_rss.html', context)


def upload(request):
    """
    If a file is uploaded, the links are read and data is put in the database
    """
    context = {}

    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

        cwd = os.getcwd()
        new_added_file = os.path.join(cwd + fs.url(name))

        old_number_of_articles_in_db = Information.objects.all()
        returnvalue = main(new_added_file)

        # If the link is valid and data is put in a text file, the file can be put in the db
        if returnvalue == "Er is data opgehaald van de link":
            main_stoppen()

        new_number_of_articles_in_db = Information.objects.all()

        toegevoegd = len(new_number_of_articles_in_db) - len(old_number_of_articles_in_db)
        context['added_to_db'] = toegevoegd
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


def show_all_filters(request):
    """
    Show a list of all searches that are done
    """
    alle_filters = Search.objects.all()
    lijst_met_onderwerpen = []

    for search in alle_filters:
        if search.search_id not in lijst_met_onderwerpen:
            lijst_met_onderwerpen.append(search.search_id)

    return render(request, 'showing_filters/show_all_filters.html', {'all_filters': alle_filters, 'lijst': lijst_met_onderwerpen})


def show_articles_with_this_filter_id(request, filter_id):
    """
    Show all articles that were found with a specific search question
    """
    query = request.GET.get('name')
    print(query)
    alle_artikelen = Search.objects.filter(search_id = filter_id)
    list = []
    for article in alle_artikelen:
        list.append(Information.objects.filter(id = article.article_id))

    return render(request, 'showing_filters/show_filter_article.html', {'ding': list})


def graph(request):
    """
    Shows js graph
    """
    from .make_json import jsonmain
    jsonmain()
    return render(request, 'graph.html')