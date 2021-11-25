
#importing functions from scraping_functions.py
import sys
#from collections import OrderedDict
sys.path.append(
    '/Volumes/GoogleDrive/My Drive/Ad Product Analytics/Web_Scraping/Merch')
from Merch_parsing_functions import *

id="B09GLXGBYQ"
HTMLFile = open("/Users/vekoppula/work/Merch/"+id+".html", "r")

# Reading the file
data_file = HTMLFile.read()



# Creating a BeautifulSoup object and specifying the parser
soup = BeautifulSoup(data_file, "html.parser")

product_title = soup.find_all("span", {"id": "productTitle"})[
    0].text.strip()
product_pirce = "".join(("$", soup.find_all(
    "span", {"class": "a-price"})[0].text.strip().split("$")[-1]))


module_container = []
for index1, module in enumerate(soup.find_all("div", {"class":"a-carousel-display-swap"})[0:1], start=1):
    module_dict = {}

    module_specs = re.sub(r"\s\s+", ",", module.find_all("h2",
                          {"class": "a-carousel-heading"})[0].text.strip()).split(",")
    module_title = module_specs[0]
    try:
        module_content_type = module_specs[1]
    except IndexError:
        module_content_type = ""
    carousel_options = json.loads(module["data-a-carousel-options"])
    items_container = []
    container = module.find("ol", {"class": "a-carousel"})
    print(index1)
    #prasing corousel items in a module
    for index2, li in enumerate(container.find_all('li', recursive=False)[0:1], start=1):
        print(index2)
        item_index = index2
        result_dict = {}
        result_dict['item_index'] = item_index
        try:
            if li.findChild("div").find_all("a")[1]['title']:
                title = li.findChild("div").find_all("a")[1]['title']
        except (IndexError,KeyError):
            if li.findChild("div").find_all("a")[1].text:
                title=li.findChild("div").find_all("a")[1].text.strip()
            else:
                title=""
        print(title)



li.findChild("div").find_all("a")[1].text
if li.findChild("div").find_all("a")[1]:
    print("Titile")
else:
    print("No Title")

        vals = merch_module_parsing(li)
        items_container.append(dict(result_dict, **vals))
        items_container





if li.findChild("div").find_all("a")[1]['title']:
    title = li.findChild("div").find_all("a")[1]['title']
elif not li.findChild("div").find_all("a")[1].text:
    title=li.findChild("div").find_all("a")[1].text.strip()
else:
    title=""

print(title)


data = merch_parsing(soup, id)


# Import Module
import os
import json
import pandas as pd
import regex as re



keys = ['request_id', 'seed_item_id', 'seed_item_title', 'seed_item_price','module_index','module_title','module_content_type','set_size','carousel_name',
'item_index','item_id','title','price','star_rating','prime_label','rating_size']
df = dict([(key, []) for key in keys])
for i in range(len(data['module_container'])):
    for j in range(len(data['module_container'][i]['items_container'])):
        df['request_id'].append(data['request_id'])
        df['seed_item_id'].append(data['seed_item_id'])
        df['seed_item_title'].append(data['seed_item_title'])
        df['seed_item_price'].append(data['seed_item_price'])
        df['module_index'].append(data['module_container'][i]['module_index'])
        df['module_title'].append(data['module_container'][i]['module_title'])
        df['module_content_type'].append(data['module_container'][i]['module_content_type'])
        df['set_size'].append(data['module_container'][i]['carousel_options']['set_size'])
        df['carousel_name'].append(data['module_container'][i]['carousel_options']['name'])
        df['item_index'].append(data['module_container'][i]['items_container'][j]['item_index'])
        df['item_id'].append(data['module_container'][i]['items_container'][j]['item_id'])
        df['title'].append(data['module_container'][i]['items_container'][j]['title'])
        df['price'].append(data['module_container'][i]['items_container'][j]['price'])
        df['star_rating'].append(data['module_container'][i]['items_container'][j]['star_rating'])
        df['prime_label'].append(data['module_container'][i]['items_container'][j]['prime_label'])
        df['rating_size'].append(data['module_container'][i]['items_container'][j]['rating_size'])

pd.DataFrame(df).to_csv('/Users/vekoppula/work/Merch/' + re.sub(r"\s+",
                                                          "",id) + '.csv', header=True, index=False)

df
