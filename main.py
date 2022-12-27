import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import random

load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")

current_date = datetime.now().strftime("%Y-%m-%d")

url = f"https://pslatecustoms.myshopify.com/admin/api/2022-10/orders.json?status=unfilfilled&created_at_min={current_date}&fields=order_number,line_items,created_at"

headers = {
    "Content-Type": "application/json",
    'X-Shopify-Access-Token': SHOPIFY_ACCESS_TOKEN
}

res = requests.get(url=url, headers=headers)

result = res.json()
orders = []


for order in result["orders"]:
    for item in order["line_items"]:
        dict_to_append = {}
        if "Paracord" in item["name"]:
            dict_to_append.update({"product_name": item["name"]})
            colors = []
            for property in item["properties"]:
                if "Color " in property["name"]:
                    if property["value"] not in colors:
                        colors.append(property["value"])
                if property["name"] == "Preview":
                    dict_to_append.update({"design": property["value"]})
                if property["name"] == "Cable Comb Color":
                    dict_to_append.update({"comb_color": property["value"]})
            dict_to_append.update({"sleeving_colors": colors})
            if colors != ["Black"]:
                orders.append(dict_to_append)

#print((json.dumps(orders, indent=4)))
print(len(orders))
randomt_int = random.randint(0, len(orders)-1)
print(randomt_int)
print((json.dumps(orders[randomt_int], indent=4)))
