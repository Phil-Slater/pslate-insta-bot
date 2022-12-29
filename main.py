import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import random
from PIL import Image
from io import BytesIO
from instagrapi import Client


load_dotenv()

SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_ACCESS_TOKEN")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_API_SECRET = os.getenv("SHOPIFY_API_SECRET")
IG_USERNAME = os.getenv("IG_USERNAME")
IG_PWD = os.getenv("IG_PWD")

current_date = datetime.now().strftime("%Y-%m-%d")

# bot = Client()
# bot.login(IG_USERNAME, IG_PWD)

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

print(
    f"Number of paracord sleeved products ordered in past day: {len(orders)}")
randomt_int = random.randint(0, len(orders)-1)
print((json.dumps(orders[randomt_int], indent=4)))

rotation_angles = [0, 10, 20, 30, 40, 320, 330, 340, 350]
random_rotation_int = random.randint(0, len(rotation_angles)-1)
print(f"Rotation angle: {rotation_angles[random_rotation_int]} degrees")

res = requests.get(orders[randomt_int]["design"])

cable_img = Image.open(BytesIO(res.content))
rotated = cable_img.rotate(
    angle=rotation_angles[random_rotation_int], expand=True)
cable_w, cable_h = rotated.size

with Image.open("template.png") as template_img:
    template_w, template_h = template_img.size
    offset = ((template_w - cable_w) // 2, (template_h - cable_h) // 2)
    template_img.alpha_composite(rotated, offset)
    template_img = template_img.convert('RGB')
    os.chdir("images")
   # template_img.save(f'{current_date}_image.jpg')

sleeving_colors = ", ".join(orders[randomt_int]["sleeving_colors"])

caption = f"""Cable of the day!
Check out our sleeved cable of the day-- ordered today by one of our customers! This is a {orders[randomt_int]["product_name"]} designed with {sleeving_colors} paracord and {orders[randomt_int]["comb_color"].lower()} cable combs!
.
.
.
.
.
#hashtags #hashtag1 #hashtag2"""

print(f"\n{caption}")

# bot.photo_upload(f'{current_date}_image.jpg', caption)
