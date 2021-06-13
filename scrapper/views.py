from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
# Create your views here.
def home(requests):
    return render(requests, 'scrapper/base.html')

def new_search(requests):
    search=requests.POST.get('search')
    print(search)
    stuff_for_frontend={
        'search':search,
    }
    return render(requests,'scrapper/new_search.html',stuff_for_frontend)