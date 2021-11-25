#importing functions from scraping_functions.py
import json
import sys
#from collections import OrderedDict
sys.path.append(
    '/Volumes/GoogleDrive/My Drive/Ad Product Analytics/Web_Scraping/Merch')
from Merch_parsing_functions import *
from Merch_scraping_json_to_csv import *

items = ["B09GLXGBYQ","B089T61XRG","B07GB3FNNV","B092Z9GDXW","B07BFS3G7P","B06XKCZYXK","B08CLSXJSW","B08MXWFRKM","B084TM4XKG"]

for id in items:
    # create the driver object.
    driver = configure_driver()
    #search_keyword = "iPhone"
    soup = getCourses(driver, id)
    # close the driver.

    try:
        data = merch_parsing(soup, id)
        flatten_results_dic(data, id)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("There is an error occured for the item_id: ", id)

    driver.close()
