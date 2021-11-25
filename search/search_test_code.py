
#importing functions from scraping_functions.py
import sys
sys.path.append('/Volumes/GoogleDrive/My Drive/Ad Product Analytics/Web_Scraping')
from scraping_functions import *


HTMLFile = open("/Users/vekoppula/work/sweaters for men.html", "r")

# Reading the file
index = HTMLFile.read()

# Creating a BeautifulSoup object and specifying the parser
soup = BeautifulSoup(index, "html.parser")


rid_pattern=re.compile('\"requestId\":\"(.*?)\"')
request_id=re.findall(rid_pattern, str(soup))[0]
pattern  = re.compile('data-index=(\".*?\")')
indexes=re.findall(pattern, str(soup))
indexes  =','.join([i.replace('"', '') for i in indexes])
indexes=indexes.split(",")



parsing_func_dict = {"SEARCH_RESULTS": parse_search_results, "VISUAL_NAVIGATION": parse_visual_navigation,
                     "FEATURED_ASINS_LIST": featured_asins_list, "SHOPPING_ADVISER": shopping_adviser,
                     "TAB_NAVIGATION": tab_navigation, "CARDS": cards}
widgets_data=[]
for widget_indx, i in enumerate(indexes[1:5], start=1):
    if i:
        result=soup.find_all("div", {"data-index":i})[0]
        #print(result)
        row=result
        widget_indx=widget_indx
        # if upper slot is blank then div else span
        if soup.find_all("div", {"class":"slot=UPPER"}):
            tag="div"
        else:
            tag="span"

        #widget_id
        for x in row.find_all(tag,{"class":"slot=MAIN"})[0]['class']:
            if "widgetId=" in x:
                widgetId=x.split("=")[1]
        #template_id
        for x in row.find_all(tag,{"class":"slot=MAIN"})[0]['class']:
            if "template=" in x:
                template=x.split("=")[1]
                print(template)

        if template in parsing_func_dict.keys():
            result_dict = {}
            result_dict['widget_indx'] = widget_indx
            result_dict['widgetId'] = widgetId
            result_dict['template'] = template
            vals = parsing_func_dict[template](row)
            widgets_data.append(dict(result_dict, **vals[0]))
        else:
            vals = [{'widgetId': widgetId}, {'template': template}]
            result_dict = {}
            result_dict['widget_indx'] = widget_indx
            result_dict['widgetId'] = widgetId
            result_dict['template'] = template
            widgets_data.append(dict(result_dict, **vals[0]))







if template in parsing_func_dict.keys():
    result_dict = {}
    result_dict['widgetId'] = widgetId
    result_dict['template'] = template
    vals = parsing_func_dict[template](row)
    widgets_data.append(dict(result_dict, **vals[0]))
else:
    vals = [{'widgetId': widgetId}, {'template': template}]
    result_dict = {}
    result_dict['widgetId'] = widgetId
    result_dict['template'] = template
    widgets_data.append(dict(result_dict, **vals[0]))


parsing_func_dict[template](row)

try:
    print(row.find_all('span', {'class':'a-price'})[0].text.strip())
except IndexError:
    print("no more")


# importing the libraries
from bs4 import BeautifulSoup
import requests
import regex as re

url="https://www.amazon.com/s?k=iphone"

# Make a GET request to fetch the raw HTML content
html_content = requests.get(url,verify=False)
print(html_content.status_code)

# Parse the html content
soup = BeautifulSoup(html_content.tex, "html.parser")


pattern  = re.compile('data-index=(\".*?\")')
indexes=re.findall(pattern, str(soup))
indexes  =','.join([i.replace('"', '') for i in indexes])
indexes=indexes.split(",")

indexes

type(soup)
