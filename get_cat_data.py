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

"""
page = requests.get(SITEURL)

if page.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = page.content

soup = BeautifulSoup(content, 'html.parser')
"""

allCategories = []


def get_category_url(inpt):
    "Return category url string from a category selector"
    "and category from a category selector"
    return [str(inpt[0]['href']), str(inpt[0].text).strip()]


CATEGORYSELECTOR = ('#default > div > div > div > aside > div.side_categories '
                    '> ul > li > ul > li:nth-child(0) > a')


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


"""
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
"""


"""
def extract_book(fsoup, furl):
    "extract book data from soup:fsoup of the page url:furl"
    fbook = {}
    data = fsoup.select(SELECTOR['title'])
    fbook['title'] = get_bk_title(data)
    data = fsoup.select(SELECTOR['category'])
    fbook['category'] = get_bk_category(data)
    data = fsoup.select(SELECTOR['upc'])
    fbook['upc'] = get_bk_upc(data)
    data = fsoup.select(SELECTOR['incltax'])
    fbook['incltax'] = get_bk_incltax(data)
    data = fsoup.select(SELECTOR['excltax'])
    fbook['excltax'] = get_bk_excltax(data)
    data = fsoup.select(SELECTOR['stock'])
    fbook['stock'] = get_bk_stock(data)
    data = fsoup.select(SELECTOR['rating'])
    fbook['rating'] = get_bk_rating(data)
    fbook['url'] = get_bk_url(furl)
    data = fsoup.select(SELECTOR['img'])
    fbook['img'] = get_bk_img(data)
    data = fsoup.select(SELECTOR['description'])
    fbook['description'] = get_bk_description(data)
    return fbook
"""


def extract_book(fsoup, furl):
    "extract book data from soup:fsoup of the page url:furl"
    fbook = []
    data = fsoup.select(SELECTOR['title'])
    fbook.append(get_bk_title(data),)
    data = fsoup.select(SELECTOR['category'])
    fbook.append(get_bk_category(data),)
    data = fsoup.select(SELECTOR['upc'])
    fbook.append(get_bk_upc(data),)
    data = fsoup.select(SELECTOR['incltax'])
    fbook.append(get_bk_incltax(data),)
    data = fsoup.select(SELECTOR['excltax'])
    fbook.append(get_bk_excltax(data),)
    data = fsoup.select(SELECTOR['stock'])
    fbook.append(get_bk_stock(data),)
    data = fsoup.select(SELECTOR['rating'])
    fbook.append(get_bk_rating(data),)
    fbook.append(get_bk_url(furl),)
    data = fsoup.select(SELECTOR['img'])
    fbook.append(get_bk_img(data),)
    data = fsoup.select(SELECTOR['description'])
    fbook.append(get_bk_description(data),)
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

"""
List all categories.Not used so far. Will be when iterating through the whole
site
for i in range(1, 51):
    categorySelector = CATEGORYSELECTOR.replace("0", str(i))
    catData = soup.select(categorySelector)
    allCategories.append((get_category_url(catData)))
    print(allCategories[i-1])
"""
"""
page = requests.get(SITEURL)

if page.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = page.content

soup = BeautifulSoup(content, 'html.parser')
"""


filename = 'fantasy.csv'
CATBASEURL = "https://books.toscrape.com/catalogue/category/books/fantasy_19"


def get_book_list(catBaseUrl):
    i = 1
    booklist = []
    pageHtml = "/index.html"
    while True:
        page = requests.get(catBaseUrl + pageHtml)
        if page.status_code != 200:
            return booklist
            print("category add-a-comment has: ", str(i-1), " pages")
            break
        else:
            content = page.content
            booklist += get_book_url(content)
            i = i + 1
            pageHtml = "/page-" + str(i) + ".html"


bookList = get_book_list(CATBASEURL)

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
#    for key in book:
#        record.append(book[key], )
#    rows.append(record)
    rows.append(book)

recordWriter = csv.writer(open(filename, 'w', newline=''))
recordWriter.writerow(CSVHEADER)
recordWriter.writerows(rows)
