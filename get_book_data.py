import requests
from bs4 import BeautifulSoup

siteUrl = 'http://books.toscrape.com/'
url = siteUrl + 'catalogue/a-light-in-the-attic_1000/index.html'

print()
print(url)
print()

bookRecord = []
book = {}

page = requests.get(url)

if page.status_code != 200:
    print("Error fetching page")
    exit()
else:
    content = page.content

soup = BeautifulSoup(content, 'html.parser')

TITLESELECTOR = ('head > title')
CATEGORYSELECTOR = ('#default > div > div > ul > li:nth-child(3) > a')
UPCSELECTOR = ('#content_inner > article > table > tr:nth-child(1) > td')
WITHTAXSELECTOR = ('#content_inner > article > table > tr:nth-child(4) > td')
WITHOUTTAXSELECTOR = ('#content_inner > article > table > tr:nth-child(3) > '
                      'td')
STOCKSELECTOR = ('#content_inner > article > div.row >'
                 'div.col-sm-6.product_main > p.instock.availability')
RATINGSELECTOR = ('#content_inner > article > div.row >'
                  'div.col-sm-6.product_main > p.star-rating.Three')
IMAGEURLSELECTOR = ('#product_gallery > div > div > div > img')

DESCRIPTIONSELECTOR = ('head > meta:nth-child(4)')

# 0
titleData = soup.select(TITLESELECTOR)

book['title'] = str(titleData[0].
                    text.
                    replace(" | Books to Scrape - Sandbox", "").
                    strip())

bookRecord.append(book['title'])

print(book['title'])
print()


# 1
categoryData = soup.select(CATEGORYSELECTOR)

book['category'] = str(categoryData[0].
                       text)

bookRecord.append(book['category'])

print(book['category'])
print()

# 2
upcData = soup.select(UPCSELECTOR)

book['upc'] = str(upcData[0].
                  text)

bookRecord.append(book['upc'])

print(book['upc'])
print()

# 3
WithTaxData = soup.select(WITHTAXSELECTOR)

book['withTax'] = str(WithTaxData[0].
                      text)


bookRecord.append(book['withTax'])

print(book['withTax'])
print()


# 4
WithoutTaxData = soup.select(WITHOUTTAXSELECTOR)

book['withoutTax'] = str(WithoutTaxData[0].
                         text)


bookRecord.append(book['withoutTax'])

print(book['withoutTax'])
print()

# 5
stockData = soup.select(STOCKSELECTOR)

book['stock'] = (stockData[0].
                 text.
                 strip().
                 replace("In stock (", "").
                 replace(" available)", ""))

bookRecord.append(book['stock'])

print(book['stock'])
print()

# 6
ratingData = soup.select(RATINGSELECTOR)

book['rating'] = (ratingData[0]['class'][1])

bookRecord.append(book['rating'])

print(book['rating'])
print()

# 7

book['url'] = url

bookRecord.append(book['url'])

print(book['url'])
print()

# 8
imageUrlData = soup.select(IMAGEURLSELECTOR)

book['imageUrl'] = ('http://books.toscrape.com' +
                    imageUrlData[0]['src'].
                    replace("../..", ""))

bookRecord.append(book['imageUrl'])

print(book['imageUrl'])
print()

# 9

descriptionData = soup.select(DESCRIPTIONSELECTOR)

book['description'] = (descriptionData[0]['content'].
                       strip())

bookRecord.append(book['description'])

print(book['description'])
print()

csvHeader = ('title, '
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
    outf.write(csvHeader)
    for key in book:
        record += (book[key] + ',')
    record += '\n'
    outf.write(record)
