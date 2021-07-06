import requests
from bs4 import BeautifulSoup

siteUrl = 'http://books.toscrape.com/'
url = siteUrl + 'catalogue/a-light-in-the-attic_1000/index.html'

print()
print(url)
print()

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
                      'div.col-sm-6.product_main > p.star-rating.Three')

SELECTOR['url'] = ('')

SELECTOR['img'] = ('#product_gallery > div > div > div > img')

SELECTOR['description'] = ('head > meta:nth-child(4)')


def get_title(inpt):
    """Return title string from a title selector"""
    return str(inpt[0].
               text.
               replace(" | Books to Scrape - Sandbox", "").
               strip())


def get_category(inpt):
    """Return category string from a category selector"""
    return str(inpt[0].
               text)


def get_upc(inpt):
    """Return upc string from a upc` selector"""
    return str(inpt[0].
               text)


def get_incltax(inpt):
    """Return price string from a price including tax selector"""
    return str(inpt[0].
               text)


def get_excltax(inpt):
    """Return price string from a price excluding selector"""
    return str(inpt[0].
               text)


def get_stock(inpt):
    """Return stock string from a stock selector"""
    return (inpt[0].
            text.
            strip().
            replace("In stock (", "").
            replace(" available)", ""))


def get_rating(inpt):
    """Return rating string from a rating selector"""
    return (inpt[0]['class'][1])


def get_url(inpt):
    """Return url string"""
    return inpt


def get_img(inpt):
    """Return image url string from a image url selector"""
    return ('http://books.toscrape.com' +
            inpt[0]['src'].
            replace("../..", ""))


def get_description(inpt):
    """Return description string from a description selector"""
    return (inpt[0]['content'].
            strip())


for key in SELECTOR:
    if key != 'url':
        data = soup.select(SELECTOR[key])
    if key == 'title':
        book[key] = get_title(data)
    elif key == 'category':
        book[key] = get_category(data)
    elif key == 'upc':
        book[key] = get_upc(data)
    elif key == 'incltax':
        book[key] = get_incltax(data)
    elif key == 'excltax':
        book[key] = get_excltax(data)
    elif key == 'stock':
        book[key] = get_stock(data)
    elif key == 'rating':
        book[key] = get_rating(data)
    elif key == 'url':
        book[key] = get_url(url)
    elif key == 'img':
        book[key] = get_img(data)
    elif key == 'description':
        book[key] = get_description(data)

CSVHEADER = ('title, '
             'category, '
             'universal_product_code, '
             'price_including_tax, '
             'price_excluding_tax, '
             'number_available, '
             'review_rating, '
             'product_page_url, '
             'image_url, '
             'product_description\n')

record = ""

with open('book.csv', 'w') as outf:
    outf.write(CSVHEADER)
    for key in book:
        record += (book[key] + ',')
    record += '\n'
    outf.write(record)
