#!/usr/bin/env python

from bs4 import BeautifulSoup
from requests_html import HTMLSession

def main_webscraping(url):
    session = HTMLSession()
    getarticle_page = session.get(url)
    soup = BeautifulSoup(getarticle_page.content,'html.parser')

    article = soup.find(id="text")
    text = article.find_all("p")

    string_met_info = ""
    for p in text:
        info = p.get_text()
        info = info.strip('"')
        info += " "
        string_met_info += info

    return string_met_info