import requests
from bs4 import BeautifulSoup
import csv
from model import Product


def parser(url:str, max_item: int):
    create_csv()
    page = 1
    count_items = 0
    while max_item > count_items:
        list_product = []
        res = requests.get(f"{url}&p={page}")
        soup = BeautifulSoup(res.text, "lxml")
        products = soup.find_all("div", class_="product-card")

        for product in products:
            if count_items >= max_item:
                break
            count_items += 1
            name = product.get("data-product-name")
            sku = product.find("span", class_ = "product-card__key").text
            name_elem = product.find("meta", itemprop="name")
            link = name_elem.findNext().get("href")
            price_elem = product.find("span", itemprop="price")
            if price_elem:
                price = price_elem.get("content")
            else:
                price = "По запросу"
            list_product.append(Product(sku=sku,
                                        name=name,
                                        link=link,
                                        price=price))
        write_csv(list_product)
        page += 1


def create_csv():
    with open(f"glavsnab.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "sku",
            "name",
            "link",
            "price"
        ])

def write_csv(products: list[Product]):
    with open(f"glavsnab.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        for product in products:
            writer.writerow([
                product.sku,
                product.name,
                product.link,
                product.price
            ])

if __name__ == "__main__":
    parser(url="https://glavsnab.net/stroymateriali/pilomateriali/vagonka.html?limit=100", max_item=268)