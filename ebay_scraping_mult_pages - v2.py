import requests
from bs4 import BeautifulSoup
import pandas as pd

ebay_items = []
#able to choose the range of pages we want to scrape
for i in range(1,5):
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=+guitar+switch+tip&_sacat=0&LH_TitleDesc=0&LH_PrefLoc=2&_pgn={i}"
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, "html.parser")  # need HTML parser to parse ebay page
    div = soup.find_all("li", class_="s-item s-item__pl-on-bottom")
    # gets the item title, URL of the item, the condition of the item, and price
    for divs in div:
        title = divs.find("span", role="heading").text
        price = divs.find("span", class_="s-item__price").text
        shipping_price = divs.find("span", class_="s-item__shipping")
        condition = divs.find("span", class_="SECONDARY_INFO").text
        item_url = divs.find("a", href=True)  # finds all href
        #Shipping price kept returning type as None with .text
        #So we do an if guard below to get it to append properly
        if shipping_price is not None:
            shipping_price = shipping_price.text
            #print(shipping_price)
            ebay_items.append([title, price, shipping_price, condition, item_url['href']])

        # appends only the href for item_url that we need for the items

df = pd.DataFrame(ebay_items, columns=['Title', 'Price', 'Shipping Price', 'Condition', 'URL'])
df.to_csv('ebay_items.csv')
