import requests
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.emag.bg/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

# Get the html
k = requests.get("https://www.emag.bg/mobilni-telefoni/sort-discountdesc/c").text
soup = BeautifulSoup(k, 'html.parser')

# Get all the products on the page (could also use a custom limit)
productlist = soup.find_all("div", class_="card-item card-standard js-product-data", limit=10)
productlinks = []
for product in productlist:
    # Get the link to each product page
    link = product.find("a",{"class":"card-v2-title semibold mrg-btm-xxs js-product-url"}).get('href')
    productlinks.append(link)

data = []
for link in productlinks:
    f = requests.get(link,headers=headers).text
    hun = BeautifulSoup(f, 'html.parser')
    
    try:
        name = hun.find("h1", {"class":"page-title"}).text.replace('\n',"")
    except:
        name = None
    
    try:
        price = hun.find("p",{"class":"product-new-price"}).text.replace('\n',"")
    except:
        price = None

    phone = {"name":name,"price":price}
    data.append(phone)

# Condense and display the data in a readable table
pd.set_option("display.max_colwidth", 10000)
df = pd.DataFrame(data)
print(df)