# importing functions
import sys
sys.path.append(
    '/Volumes/GoogleDrive/My Drive/Ad Product Analytics/Web_Scraping')
from search_scraping_json_to_csv import *
from scraping_functions import *

sks = ['Kids Backpack', 'iphone', 'X-box', 'sweaters for men']

for search_keyword in sks:
    # create the driver object.
    driver = configure_driver()
    #search_keyword = "iPhone"
    soup = getCourses(driver, search_keyword)
    # close the driver.

    try:
        data = parsing_logic(soup, search_keyword)
        flatten_results_dic(data, search_keyword)
    except:
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])
        print("There is an error occured for the keyword: ", search_keyword)

    driver.close()
