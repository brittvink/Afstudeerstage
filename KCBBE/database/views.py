from django.shortcuts import render
from .models import Information
from django.db import connection
from django.db.models import Q
from plotly.offline import plot
import plotly.express as px
import pandas as pd
from django.http import HttpResponseRedirect
from .lezen_van_rss import main
from .stoppen_in_database import main_stoppen
from django.core.files.storage import FileSystemStorage
from .uploaded_file.read_file import main_read_file
import os
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render


# Create your views here.
def home(request):
    return render(request, 'home.html')


def titles(request):
    title_list = Information.objects.all().order_by('title')
    return render(request, 'title_list.html', {'title_list': title_list})


def search_titles(request):
    if request.method == "POST":
        searched_title = request.POST['searched']
        searched_topic = request.POST['searched-topic']
        searched_topic = searched_topic.split(' ')
        searched_title = searched_title.split(' ')

        searched_dict = {"title": searched_title, "summary": searched_topic}
        query = Q()

        for topic in searched_topic:
            query = query & Q(summary__icontains=topic)

        for word in searched_title:
            query = query & Q(title__icontains=word)

        titles = Information.objects.filter(query).order_by('title')
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
            return render(request, 'text_field_rss.html')
        else:
            # return render(request, 'upload.html')
            return redirect('upload/')

    return render(request, 'read_rss.html')


def text_field_rss(request):
    if request.method == "POST":
        rss = request.POST['rss']
        print(rss)
        main(rss)
        alles = main_stoppen()
        return render (request, 'after_rss.html', {'rss': alles})
    else:
        return render(request, 'read_rss.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)

        cwd = os.getcwd()
        new_added_file = os.path.join(cwd + fs.url(name))
        
        main_read_file(new_added_file)
    
        alles = main_stoppen()
        return render(request, 'after_rss.html', {'rss': alles})

    return render(request, 'upload.html', context)
