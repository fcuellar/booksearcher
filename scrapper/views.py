from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from . import models
# Create your views here.
BASE_CRAGLIST_URL='https://www.booksamillion.com/search?filter=&id=8236417472614&query={}'
def home(request):
    return render(request, 'scrapper/base.html')

def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_CRAGLIST_URL.format(quote_plus(search))
    print(final_url)
    response=requests.get(final_url)
    data=response.text
    soup = BeautifulSoup(data,features='html.parser')
    book_listings=soup.find_all('div',{'class':'search-result-item'})
    """ book_title=post_titles[0].find('a').get('title')
    book_link=post_titles[0].find('a').get('href')
    img_link=post_titles[0].find('img').get('src')
    """
    price=book_listings[0].find(class_='our-price').text
    print(price[2:])
    final_books=[]
    bugimagecounter=0
    for books in book_listings:
        bugimagecounter+=1
        book_title=books.find('a').get('title')
        book_link=books.find('a').get('href')
        if(bugimagecounter<8):
            img_link=books.find('img').get('src')
        elif (bugimagecounter>8):
            img_link=books.find('img').get('data-src')
        book_price=books.find(class_='our-price').text
        #book_price=float(book_price[2:])
        final_books.append((book_title,book_link,img_link,book_price))
    #For Sorting in ascending order
    #final_books.sort(key = lambda x: x[3])
    #print(data)

    stuff_for_frontend={
        'search':search,
        'final_books':final_books,
    }
    return render(request,'scrapper/new_search.html',stuff_for_frontend)