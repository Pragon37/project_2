"""
Find out the different bokk categories and will collect book data
for one one these category possibly spanning through several web pages
"""
import csv
import requests
from bs4 import BeautifulSoup

SITEURL = 'http://books.toscrape.com/'
url = SITEURL + 'catalogue/a-light-in-the-attic_1000/index.html'

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

print()
print(url)
print()

book = {}
SELECTOR = {}

page = requests.get(SITEURL)

if page.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = page.content

soup = BeautifulSoup(content, 'html.parser')

allCategories = []


def get_category_url(inpt):
    "Return category url string from a category selector"
    return [str(inpt[0]['href']), str(inpt[0].text).strip()]


CATEGORYSELECTOR = ('#default > div > div > div > aside > div.side_categories '
                    '> ul > li > ul > li:nth-child(0) > a')

for i in range(1, 51):
    categorySelector = CATEGORYSELECTOR.replace("0", str(i))
    catData = soup.select(categorySelector)
    allCategories.append((get_category_url(catData)))

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


def get_bk_title(inpt):
    "Return title string from a title selector"
    return str(inpt[0].
               text.
               replace(" | Books to Scrape - Sandbox", "").
               strip())


def get_bk_category(inpt):
    "Return category string from a category selector"
    return str(inpt[0].
               text)


def get_bk_upc(inpt):
    "Return upc string from a upc` selector"
    return str(inpt[0].
               text)


def get_bk_incltax(inpt):
    "Return price string from a price including tax selector"
    return str(inpt[0].
               text)


def get_bk_excltax(inpt):
    "Return price string from a price excluding selector"
    return str(inpt[0].
               text)


def get_bk_stock(inpt):
    "Return stock string from a stock selector"
    return (inpt[0].
            text.
            strip().
            replace("In stock (", "").
            replace(" available)", ""))


def get_bk_rating(inpt):
    "Return rating string from a rating selector"
    return (inpt[0]['class'][1])


def get_bk_url(inpt):
    "Return url string"
    return inpt


def get_bk_img(inpt):
    "Return image url string from a image url selector"
    return ('http://books.toscrape.com' +
            inpt[0]['src'].
            replace("../..", ""))


def get_bk_description(inpt):
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
            fbook[key] = get_bk_title(data)
        elif key == 'category':
            fbook[key] = get_bk_category(data)
        elif key == 'upc':
            fbook[key] = get_bk_upc(data)
        elif key == 'incltax':
            fbook[key] = get_bk_incltax(data)
        elif key == 'excltax':
            fbook[key] = get_bk_excltax(data)
        elif key == 'stock':
            fbook[key] = get_bk_stock(data)
        elif key == 'rating':
            fbook[key] = get_bk_rating(data)
        elif key == 'url':
            fbook[key] = get_bk_url(furl)
        elif key == 'img':
            fbook[key] = get_bk_img(data)
        elif key == 'description':
            fbook[key] = get_bk_description(data)
    return fbook


def get_book_url(pageContent):
    "Find all the book urls in pageContent"
    urlList = []
    pageSoup = BeautifulSoup(pageContent, 'html.parser')
    i = 1
    while True:
        bookUrlSelector = ('#default > div > div > div > div > section >'
                           ' div:nth-child(2) > ol > li:nth-child(0) > article'
                           ' > h3 > a').replace("0", str(i))
        bookUrl = pageSoup.select(bookUrlSelector)
        if bookUrl != []:
            i = i + 1
            print(str(bookUrl[0]['href']))
            urlList.append(str(bookUrl[0]['href']))
        else:
            print(i-1)
            return urlList
            break


page = requests.get("https://books.toscrape.com/catalogue/category/books/mystery_3/index.html")
content = page.content
bookList = get_book_url(content)


rows = []

for i in bookList:
    record = []
    url = "https://books.toscrape.com/catalogue" + i.replace("../../..", "")
    print(url)
    page = requests.get(url)

    if page.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        content = page.content

    soup = BeautifulSoup(content, 'html.parser')
    book = extract_book(soup, url)
    for key in book:
        record.append(book[key], )
    rows.append(record)

recordWriter = csv.writer(open('book_cat.csv', 'w', newline=''))
recordWriter.writerow(CSVHEADER)
recordWriter.writerows(rows)
