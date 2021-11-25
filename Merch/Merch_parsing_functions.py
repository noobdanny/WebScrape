import time
import regex as re
from collections import OrderedDict
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def configure_driver():
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    # Instantiate the Webdriver: Mention the executable path of the webdriver you have downloaded
    # For linux/Mac
    driver = webdriver.Chrome(
        '/Users/vekoppula/Downloads/chromedriver', options=chrome_options)
    return driver


def getCourses(driver, id):
    driver.get("https://www.amazon.com/dp/" + id)
    # wait for the element to load
    try:
        time.sleep(2)
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None
    with open("/Users/vekoppula/work/Merch/" + id + ".html", "w") as f:
        f.write(driver.page_source)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup

# function to parase merch modules


def merch_module_parsing(tag):
    try:
        item_id_pattern = re.compile('data-asin=(\".*?\")')
        if re.findall(item_id_pattern, str(tag)):
            item_id = re.findall(item_id_pattern, str(tag))[0].strip('"')
        else:
            item_id = tag.findChild("div").find_all(
                "a")[0]['href'].split("&")[-2].split("=")[-1]
    except (TypeError, AttributeError, IndexError):
        item_id = ""
    try:
        if tag.findChild("div").find_all("a")[1]['title']:
            title = tag.findChild("div").find_all("a")[1]['title']
    except (IndexError,KeyError):
        if tag.findChild("div").find_all("a")[1].text:
            title=tag.findChild("div").find_all("a")[1].text.strip()
        else:
            title=""
    try:
        if tag.find("i", {"class": "a-icon-star"}):
            star_rating = re.findall(
                '"([^"]*)"', str(tag.find("i", {"class": "a-icon-star"})))[0].split(" ")[-1]
        else:
            star_rating = tag.find("i").text.strip()
    except IndexError:
        star_rating = ""
    try:
        if tag.find("i", {"class": "a-icon-star"}):
            rating_size = tag.find(
                "span", {"class": "a-color-link"}).text.strip()
        else:
            rating_size = tag.find_all(
                "span", {"class": "a-size-small"})[0].text.strip()
    except IndexError:
        rating_size = ""
    try:
        if tag.find_all("span", {"class": "a-price-range"}):
            price = tag.find_all("span", {"class": "a-price"})[0].findChild("span").text.strip(
            ) + "-" + tag.find_all("span", {"class": "a-price"})[1].findChild("span").text.strip()
        elif tag.find("span", {"class": "a-color-price"}):
            price = tag.find("span", {"class": "a-color-price"}).text.strip()
        else:
            price = "".join(
                ("$", tag.find("span", {"class": "a-price"}).text.strip().split("$")[-1]))
    except (IndexError, AttributeError):
        print("There is an error with price tag")
        price = ""
    try:
        if tag.find("i", {"class": "a-icon-prime"}):
            prime_label = "Yes"
        else:
            prime_label = "No"
    except IndexError:
        prime_label = ""
    vals = {
        'item_id': item_id,
        'title': title,
        'price': price,
        'star_rating': star_rating,
        'prime_label': prime_label,
        'rating_size': rating_size,

    }
    return vals

# prasing logic for the entire merch page


def merch_parsing(soup, id):
    rid_pattern = re.compile('\"requestId\":\"(.*?)\"')
    request_id = re.findall(rid_pattern, str(soup))[0]
    product_title = soup.find_all("span", {"id": "productTitle"})[
        0].text.strip()
    product_pirce = "".join(("$", soup.find_all(
        "span", {"class": "a-price"})[0].text.strip().split("$")[-1]))

    module_container = []
    for index1, module in enumerate(soup.find_all("div", {"class":"a-carousel-display-swap"}), start=1):
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
        #prasing corousel items in a module
        for index2, li in enumerate(container.find_all('li', recursive=False), start=1):
            item_index = index2
            result_dict = {}
            result_dict['item_index'] = item_index
            vals = merch_module_parsing(li)
            items_container.append(dict(result_dict, **vals))

        module_dict['module_index'] = index1
        module_dict['module_title'] = module_title
        module_dict['module_content_type'] = module_content_type
        module_dict['carousel_options'] = carousel_options
        module_dict['items_container'] = items_container
        module_container.append(module_dict)

    final_result_dict = {}
    final_result_dict['request_id'] = request_id
    final_result_dict['seed_item_id'] = id
    final_result_dict['seed_item_title'] = product_title
    final_result_dict['seed_item_price'] = product_pirce
    final_result_dict['module_container'] = module_container
    with open('/Users/vekoppula/work/Merch/' + re.sub(r"\s+", "", id) + '.json', 'w') as outfile:
        json.dump(final_result_dict, outfile)
    return final_result_dict
