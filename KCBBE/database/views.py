from .models import Information
from django.db import connection
from django.db.models import Q
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from django.http import HttpResponseRedirect, HttpResponse
from .lezen_van_rss import main
from .stoppen_in_database import main_stoppen
from django.core.files.storage import FileSystemStorage
import os
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InformationSerializers
from .save_searched_in_db import main_search


# Create your views here.
def home(request):
    return render(request, 'home.html')


def titles(request):
    title_list = Information.objects.all().order_by('title')
    print(len(title_list))
    return render(request, 'title_list.html', {'title_list': title_list})


def search_titles(request):
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

        # Add search data to db
        main_search(searched_topic, searched_title, titles)

        # Return
        return render(request,
            'search_titles.html',
            {'searched': searched_dict, 'articles': titles})

    else:
        return render(request, 'search_titles.html', {})


def show_article(request, article_id):
    article = Information.objects.get(pk=article_id)
    return render(request, 'show_article.html', {'article': article})




def read_rss(request):
    if request.method == "POST":
        if request.POST.get('action') == "fill_txt_field":
            return redirect('text-field-rss')
        else:
            return redirect('upload/')

    return render(request, 'read_rss.html')


def text_field_rss(request):
    context = {}
    if request.method == "POST":
        rss = request.POST['rss']
        eerst = Information.objects.all()

        returnvalue = main(rss)
        if returnvalue == "Er is data opgehaald van de link":
            main_stoppen()
            print("XXXX")

        nu = Information.objects.all()

        toegevoegd = len(nu) - len(eerst)
        context['added_to_db'] = toegevoegd

        context['return_value'] = returnvalue
    return render(request, 'text_field_rss.html', context)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

        cwd = os.getcwd()
        new_added_file = os.path.join(cwd + fs.url(name))

        eerst = Information.objects.all()
        returnvalue = main(new_added_file)

        if returnvalue == "Er is data opgehaald van de link":
            main_stoppen()

        nu = Information.objects.all()

        toegevoegd = len(nu) - len(eerst)
        context['added_to_db'] = toegevoegd

        context['return_value'] = returnvalue

    return render(request, 'upload.html', context)




class articleList(APIView):
    def get(self, request):
        articles = Information.objects.all()
        serializer = InformationSerializers(articles, many=True)
        return Response(serializer.data)
    def post(self):
        pass

