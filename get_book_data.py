"""
Read and parse a book html page. Extract the requested data and print them
in file book.csv
"""
import csv
import requests
from bs4 import BeautifulSoup

siteUrl = 'http://books.toscrape.com/'
url = siteUrl + 'catalogue/a-light-in-the-attic_1000/index.html'

print(url)

book = {}
SELECTOR = {}

page = requests.get(url)

if page.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = page.content

soup = BeautifulSoup(content, 'html.parser')

SELECTOR['title'] = ('head > title')

SELECTOR['category'] = ('#default > div > div > ul > li:nth-child(3) > a')

SELECTOR['upc'] = ('#content_inner > article > table > tr:nth-child(1) > td')

SELECTOR['incltax'] = ('#content_inner > article > table > tr:nth-child(4)'
                       ' > td')

SELECTOR['excltax'] = ('#content_inner > article > table > tr:nth-child(3)'
                       ' > td')

SELECTOR['stock'] = ('#content_inner > article > div.row >'
                     'div.col-sm-6.product_main > p.instock.availability')

SELECTOR['rating'] = ('#content_inner > article > div.row >'
                      'div.col-sm-6.product_main > p:nth-child(4)')

SELECTOR['url'] = ('')

SELECTOR['img'] = ('#product_gallery > div > div > div > img')

SELECTOR['description'] = ('head > meta:nth-child(4)')


def get_title(inpt):
    "Return title string from a title selector"
    return str(inpt[0].
               text.
               replace(" | Books to Scrape - Sandbox", "").
               strip())


def get_category(inpt):
    "Return category string from a category selector"
    return str(inpt[0].
               text)


def get_upc(inpt):
    "Return upc string from a upc` selector"
    return str(inpt[0].
               text)


def get_incltax(inpt):
    "Return price string from a price including tax selector"
    return str(inpt[0].
               text)


def get_excltax(inpt):
    "Return price string from a price excluding selector"
    return str(inpt[0].
               text)


def get_stock(inpt):
    "Return stock string from a stock selector"
    return (inpt[0].
            text.
            strip().
            replace("In stock (", "").
            replace(" available)", ""))


def get_rating(inpt):
    "Return rating string from a rating selector"
    return (inpt[0]['class'][1])


def get_url(inpt):
    "Return url string"
    return inpt


def get_img(inpt):
    "Return image url string from a image url selector"
    return ('http://books.toscrape.com' +
            inpt[0]['src'].
            replace("../..", ""))


def get_description(inpt):
    "Return description string from a description selector"
    return (inpt[0]['content'].
            strip())


def extract_book(fsoup, furl):
    "extract book data from soup:fsoup of the page url:furl"
    fbook = {}
    for key in SELECTOR:
        if key != 'url':
            data = fsoup.select(SELECTOR[key])
        if key == 'title':
            fbook[key] = get_title(data)
        elif key == 'category':
            fbook[key] = get_category(data)
        elif key == 'upc':
            fbook[key] = get_upc(data)
        elif key == 'incltax':
            fbook[key] = get_incltax(data)
        elif key == 'excltax':
            fbook[key] = get_excltax(data)
        elif key == 'stock':
            fbook[key] = get_stock(data)
        elif key == 'rating':
            fbook[key] = get_rating(data)
        elif key == 'url':
            fbook[key] = get_url(furl)
        elif key == 'img':
            fbook[key] = get_img(data)
        elif key == 'description':
            fbook[key] = get_description(data)
    return fbook


book = extract_book(soup,url)

CSVHEADER = ['title',
             'category',
             'universal_product_code',
             'price_including_tax',
             'price_excluding_tax',
             'number_available',
             'review_rating',
             'product_page_url',
             'image_url',
             'product_description']

record = []
"""
with open('book.csv', 'w') as outf:
    outf.write(CSVHEADER)
    for key in book:
        record += ((book[key]) + ',')
    record += '\n'
    outf.write(record)
"""

for key in book:
    record.append(book[key], )

csvWriter = csv.writer(open('book.csv', 'w', newline='', encoding='utf-8'))
csvWriter.writerow(CSVHEADER)
csvWriter.writerow(record)
