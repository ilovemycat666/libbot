import urllib
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import time

ua = UserAgent()

def search(query):
#USER INPUT
    query = urllib.parse.quote_plus(query[6:])
    books = "https://www.goodreads.com/search?q={}".format(query)
#TESTING CONNECTION
    while True:
        try:
            response = requests.get(books, {"User-Agent": ua.random})
            if response.status_code == 200:
                return response
        except Exception as e:
            print('Status: ', end='')
            print(e)
            time.sleep(5)
            print("Connecting...")
            continue

def cook(response):
#MAKING SOUP
    soup = BeautifulSoup(response.text, "html.parser")
    a = soup.find_all(class_='bookTitle')
    b = soup.find_all(class_='authorName')
    # c = soup.find_all(class_='greyText smallText uitext')
    results = [{'title': '!{}'.format(i+1) + entry.get_text(),
                'link': entry.get('href'),
                'author' : b[i].get_text()}
                # 'date' : c[i].get_text()}
                for i, entry in zip(range(5), a)][:5]
    return results
# Returns 'books'

def search2(books):
#TESTING CONNECTION
    while True:
        try:
            response = requests.get('https://www.goodreads.com{}'.format(books), {"User-Agent": ua.random})
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
        except KeyboardInterrupt or Exception as e:
            print('Status: ', end='')
            print(e)
            time.sleep(5)
            print("Connecting...")
            continue

def bookdetails(books, soup):
#AUTHOR
    author_div = soup.find('a', class_="authorName")
    author = author_div.find('span')
    auth = author.get_text()
#TITLE
    title = soup.find(id='bookTitle')
    titl = title.get_text().replace("\n", "").replace("      ", "")
#PUBLICATION DATE
    date = "Date: N/a"
    datePub = soup.find_all('nobr', class_="greyText")
    if datePub:
        date = datePub[0].get_text()
        date = date.strip()[17:][:-1]
    elif len(datePub) == 0:
        Publish = soup.find_all('div', class_='row')
        for i in Publish:
            pub = i.get_text().replace('\n', '').replace('      ', '')
            if pub.startswith("Published"):
                date = pub
                date = date.strip()[10:]
                break
#DESCRIPTION
    try:
        description = soup.find(id='description')
        desc = description.find_all('span')
        def count():
            if len(desc) < 2:
                return desc[0].get_text(separator="")
            elif len(desc) > 1:
                return desc[1].get_text(separator="")
        info = count()
        def length(info):
            if len(info) >= 1800:
                return '{}... \n\nMore Details: https://www.goodreads.com{}'.format(info[:1500], books)
            else:
                return '{}\n\nMore Details: https://www.goodreads.com{}'.format(info, books)
        info = length(info)
    except:
        info = "Description: N/a"
#IMAGE
    try:
        imag = soup.find('img', id="coverImage")['src']
    except:
        imag = 'Cover Image: N/a'
    info = info.strip()
    return [titl, date, auth, info, imag]

