from django.shortcuts import render
from bs4 import BeautifulSoup
from requests.compat import quote_plus
import requests
from . import models
# Create your views here.
BASE_BAM_URL='https://www.booksamillion.com/search?filter=&id=8236417472614&query={}'
BASE_BNN_URL='https://www.thriftbooks.com/browse/?b.search={}'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

def home(request):
    return render(request, 'scrapper/base.html')

def new_search(request):
    #gets the user inputted search and stores into our database
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    ##quote plus will merge the search into a string 
    final_url=BASE_BAM_URL.format(quote_plus(search))
    ##requests sent to first site for scraping
    #we will use beautifulsoup to parse the html and find only the books
    response=requests.get(final_url)
    data=response.text
    soup = BeautifulSoup(data,features='html.parser')
    book_listings=soup.find_all('div',{'class':'search-result-item'})
    """ book_title=post_titles[0].find('a').get('title')
    book_link=post_titles[0].find('a').get('href')
    img_link=post_titles[0].find('img').get('src')
    """
    #price=book_listings[0].find(class_='our-price').text
    ##list of tuples for the books to be stored in, some images have different format urls so we need to switch after x images
    final_books=[]
    bugimagecounter=0

    ##scraping different site to find cheaper books
    cheaper_books=[]
    BNN_final_url=BASE_BNN_URL.format(quote_plus(search))
    response2=requests.get(BNN_final_url,headers=headers)
    data2=response2.text
    soup2 = BeautifulSoup(data2,features='html.parser')
    book_listings2=soup2.find_all('div',{'class':'AllEditionsItem-tile Recipe-default'})
   ## book2_link='https://www.barnesandnoble.com/'+book_listings2[0].find('a').get('href')

    """ book_title2=book_listings2[0].find('img').get('alt')

    book2_link='https://www.thriftbooks.com/'+book_listings2[0].find('a').get('href')

    book2_image=book_listings2[0].find('img').get('src')
    book2_price=book_listings2[0].find(class_='SearchResultListItem-dollarAmount')
 """
    #traversing the requested HTML text to find title, link, image, and price
    for cbooks in book_listings2:
        bugimagecounter+=1
        book_title2=cbooks.find('img').get('alt')
        book2_link='https://www.thriftbooks.com/'+cbooks.find('a').get('href')
        if bugimagecounter>6:

            book2_image=cbooks.find('img').get('data-src')
        else:
            book2_image=cbooks.find('img').get('src')


        ##checks to see if the book is not in stock thus it wouldn't have a price but still may show up in a site
        #if not checked it would return none for the price and cause an error
        book2_price=cbooks.find(class_='SearchResultListItem-dollarAmount')
        if book2_price is not None:
                book2_price=cbooks.find(class_='SearchResultListItem-dollarAmount').text

                cheaper_books.append((book_title2,book2_link,book2_image,book2_price))
                # print(book2_price)
                # print(book_title2)
                # print(book2_image)


    ##NEW books
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
        book_price=float(book_price[2:])
        final_books.append((book_title,book_link,img_link,book_price))
    
    #For Sorting in ascending order
    #final_books.sort(key = lambda x: x[3])
    #print(data)

    ##to be sent for the front end
    stuff_for_frontend={
        'search':search,
        'final_books':final_books,
        'cheaper_books':cheaper_books
    }
    return render(request,'scrapper/new_search.html',stuff_for_frontend)

