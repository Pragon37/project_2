"""
Find out the different bokk categories and will collect book data
for one one these category possibly spanning through several web pages
"""
import re
import csv
import requests
from bs4 import BeautifulSoup

SITEURL = 'http://books.toscrape.com/'
print(SITEURL)

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
    """
    Return category url string from a category selector
    and category from a category selector
    """
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


def download(img_url, file_name):
    "download url to file_name"
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(img_url)
        # write to file
        file.write(response.content)


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
    return inpt[0]['class'][1]


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
    """
    "extract book data from soup:fsoup of the page url:furl"
    using the CSS selector to find the data. Then it filters the
    found data to provide the reuested information.
    """
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


def get_book_url(pagecontent):
    """
    Find all the book urls in pagecontent
    Return acts as a break and terminates the loop
    """
    urllist = []
    pagesoup = BeautifulSoup(pagecontent, 'html.parser')
    j = 1
    while True:
        bookurlselector = ('#default > div > div > div > div > section >'
                           ' div:nth-child(2) > ol > li:nth-child(0) > article'
                           ' > h3 > a').replace("0", str(j))
        bookurl = pagesoup.select(bookurlselector)
        if bookurl != []:
            j = j + 1
            # print(str(bookurl[0]['href']))
            urllist.append(str(bookurl[0]['href']))
        else:
            print(str(j-1), "books on this page")
            return urllist


def get_book_list(catbaseurl):
    """
    Iterates through all pages of a category
    and returns all the book found.
    Return acts as a break and terminates the loop
    """
    k = 1
    booklist = []
    pagehtml = "/index.html"
    while True:
        page1 = requests.get(catbaseurl + pagehtml)
        if page1.status_code == 200:
            content1 = page1.content
            booklist += get_book_url(content1)
            k = k + 1
            pagehtml = "/page-" + str(k) + ".html"
        else:
            print("category add-a-comment has: ", str(k-1), " pages")
            return booklist


def format_book_data(book_list):
    """
    Using the list of book url the function get the book page
    data and format the data to prepare it for csv writer
    and download of the book images.
    """
    rows = []
    for i in book_list:
        url = ("https://books.toscrape.com/catalogue" +
               i.replace("../../..", ""))
        # print(url)
        page = requests.get(url)

        if page.status_code != 200:
            print("Error fetching page")
            exit()
        else:
            content = page.content

        soup = BeautifulSoup(content, 'html.parser')
        book = extract_book(soup, url)
        rows.append(book)
    return rows



filename = 'fantasy.csv'
CATBASEURL = "https://books.toscrape.com/catalogue/category/books/fantasy_19"
bookList = get_book_list(CATBASEURL)

categoryRows = format_book_data(bookList)

recordWriter = csv.writer(open(filename, 'w', newline=''))
recordWriter.writerow(CSVHEADER)
recordWriter.writerows(categoryRows)

print("End of csv writing.Starts downloading images")

for item in categoryRows:
    name = re.sub('\(.*$', '', item[0])
    name = re.sub('[:,&\']', '', name)
    name = re.sub(' ', '_', name)
    name = re.sub('_$', '', name)
    filename = "book_img/" + name + ".jpg"
    imgurl = item[8]
    download(imgurl, filename)
