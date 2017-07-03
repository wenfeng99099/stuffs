from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sys

#open file for writting 
f = open('result.csv', 'w')
f.write("Name, code, brand, price\n")

def is_product(tag):
    return tag.name == 'div' and tag.has_attr('class') and tag['class'][0] == 'productarea'
    
def get_name(tag):
    item_name = tag.find('p').text.replace(",", "|")
    f.write(item_name + ",")
    
def get_code(tag):
    item_code = tag.find('h2').text[-11:-1]
    f.write(item_code + ",")
    
def get_brand(tag):
    item_brand = tag.find('img').get('alt')
    f.write(item_brand + ",")

def get_price(tag):
    item_price = tag.find('p', class_='price-final').text.replace(',', '')
    f.write(item_price + "\n")
    return True
    
def get_rating(tag):
    return True
    
def process_info(tag):
    get_name(tag)
    get_code(tag)
    get_brand(tag)
    get_price(tag)
    
def get_urls(soup):
    urls = []
    try:
        pages = soup.find('div', class_='as-pagination').find_all('li')
    except AttributeError:
        print("No result for the key word/s")
        sys.exit(0)
    for p in pages:
        urls.append(p.a['href'])
    return urls

words = input("Enter key word for Canada Computer Search: ")
#open url with urlopen request
con_url = "http://www.canadacomputers.com/search_results.php?keywords="
key_words = words.split(" ")
for i in range(len(key_words)):
    if (i + 1 == len(key_words)):
        con_url = con_url + key_words[i] 
    else:
        con_url = con_url + key_words[i] + "+"

html = urlopen(con_url)

#format html to soup 
soup = BeautifulSoup(html, 'lxml')

#get search pages url from soup
urls = get_urls(soup)

#iterate through all url result of the search
for url in urls:
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    #find all class "productarea", product info stored in it 
    products = soup.find_all('div', class_='productarea')
    for p in products:
        process_info(p)
f.close()


