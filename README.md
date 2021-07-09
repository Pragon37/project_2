# project_2 : Python basics

https://github.com/Pragon37/project_2.git


## Usage
````
python -m venv env
env/Scripts/activate
pip install -r requirements.txt
mkdir book_img
````

## 1--Extracting data for a single book:

	To extract data for book located at url:
	http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html

```` 
	python get_book_data.py
```` 
        Returns file book.csv

## 2--Extracting data for all books in a category:

	To extract data for book located at url:
	https://books.toscrape.com/catalogue/category/books/fantasy_19

```` 
	python get_cat_data.py
```` 
        Returns file fantasy.csv, jpg files in directory book_img

## 3--Extracting data for all books in a site:

	To extract data for book located at url:
	https://books.toscrape.com

```` 
	python get_site_data.py
```` 
        Returns 50 files category.csv, jnd 999 jpg files in directory book_img
        There are 1000 books, but 999 book cover pictures as The Star-Touched Queen is listed
        twice.

