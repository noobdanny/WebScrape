import time
import regex as re
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


def getCourses(driver, search_keyword):
    driver.get("https://www.amazon.com/s?k=" + search_keyword)
    # wait for the element to load
    try:
        time.sleep(5)
    except TimeoutException:
        print("TimeoutException: Element not found")
        return None
    with open("/Users/vekoppula/work/" + search_keyword + ".html", "w") as f:
        f.write(driver.page_source)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "html.parser")
    return soup


# parsing search results template
def parse_search_results(vn_tag):
    try:
        item_id_pattern=re.compile('data-asin=(\".*?\")')
        item_id=re.findall(item_id_pattern, str(vn_tag))[0]
    except (TypeError, AttributeError, IndexError):
        item_id = ""
    try:
        component_type = vn_tag.find_all(
            "span", {"class": "s-label-popover-hover"})[0].text.strip()
    except IndexError:
        component_type = ""
    try:
        title = vn_tag.find_all('h2')[0].text.strip()
    except IndexError:
        title = ""
    try:
        star_rating = vn_tag.find_all('span', {'class': 'a-icon-alt'
                                               })[0].text.strip()
    except IndexError:
        star_rating = ""
    try:
        rating_size = vn_tag.find_all(
            "div", {"class": "a-row a-size-small"})[0].text.split()[-1]
    except IndexError:
        rating_size = ""
    try:
        price = "".join(("$", vn_tag.find_all(
            'span', {'class': 'a-price'})[0].text.strip().split("$")[-1]))
    except IndexError:
        price = ""
    try:
        prime_label = vn_tag.find_all(
            "i", {"class": "a-icon-prime"})[0]['aria-label']
    except IndexError:
        prime_label = ""
    try:
        badge = vn_tag.find_all('span', {'class': 'a-size-base s-cpf-badge'
                                         })[0].text.strip()
    except IndexError:
        badge = ""
    try:
        product_specs = vn_tag.find_all('div',
                                        {'class': 'sg-row s-product-specs-view'
                                         })[0].text.strip()
    except IndexError:
        product_specs = ""
    try:
        more_buying_choice = vn_tag.find_all(
            "div", {"class": "a-section a-spacing-none a-spacing-top-mini"})[0].text.strip()
    except IndexError:
        more_buying_choice = ""
    vals = [{
        'item_id': item_id,
        'component_type': component_type,
        'title': title,
        'price': price,
        'star_rating': star_rating,
        'prime_label': prime_label,
        'rating_size': rating_size,
        'badge': badge,
        'more_buying_choice': more_buying_choice,
        'product_specs': product_specs,
    }]
    return vals

# parsing visual navigation template


def parse_visual_navigation(vn_tag):
    # aria_label = row.find_all("div",{"class":"s-visual-card-navigation-carousel-title-wrapper"})[0].text.strip()
    aria_label = vn_tag.find_all(
        "div", {"class": "s-visual-card-navigation-desktop"})[0].findChild("div").text.strip()
    corosel_pattern = re.compile('data-a-carousel-options=\'({.*})\'')
    carousel_options = re.findall(corosel_pattern, str(vn_tag))[0]
    carousel_product_names = ','.join([x for x in [x.text.strip()
                                                   for x in vn_tag.find_all('a')] if x])
    vals = [{'aria_label': aria_label,
            'carousel_options': carousel_options,
             'carousel_product_names': carousel_product_names}]
    return vals

# parsing cards template


def cards(vn_tag):
    carousel_options = {}
    try:
        aria_label = vn_tag.find_all(
            "a", {"aria-hidden": "false"})[0]['aria-label']
    except IndexError:
        aria_label = ""
    try:
        carousel_details = []
        container = vn_tag.find_all("div", {"data-avar": "desc"})
        for i in container:
            carousel_details.append(i.text.strip())
    except IndexError:
        carousel_details = []
    vals = [{'aria_label': aria_label,
             'carousel_options': carousel_options,
             'carousel_product_names': carousel_details}]
    return vals

# parsing featured list template


def featured_asins_list(vn_tag):
    aria_label = vn_tag.find_all("div", {"class": "a-section"})[0].text.strip()
    corosel_pattern = re.compile('data-a-carousel-options=\'({.*})\'')
    carousel_options = re.findall(corosel_pattern, str(vn_tag))[0]
    carousel_details = []
    container = vn_tag.find("ol", {"class": "a-carousel"})
    for li in container.find_all('li', recursive=False):
        uuid = li.findChild("div")['data-uuid']
        carosuel_data = parse_search_results(li)
        carosuel_data[0]["uuid"] = uuid
        carousel_details.append(carosuel_data[0])
    vals = [{'aria_label': aria_label,
            'carousel_options': carousel_options,
             'carousel_details': carousel_details}]
    return vals

# parsing shopping adviser template


def shopping_adviser(vn_tag):
    aria_label = vn_tag.find_all(
        "div", {"class": "s-shopping-adviser-heading"})[0].text.strip()
    corosel_pattern = re.compile('data-a-carousel-options=\'({.*})\'')
    carousel_options = re.findall(corosel_pattern, str(vn_tag))[0]
    carousel_details = []
    container = vn_tag.find("ol", {"class": "a-carousel"})
    for li in container.find_all('li', recursive=False):
        uuid = li.findChild("div")['data-uuid']
        if li.find_all("div", {"class": "s-card-container"}):
            carosuel_data = parse_search_results(li)
            carosuel_data[0]["uuid"] = uuid
            carousel_details.append(carosuel_data[0])
        else:
            aria_label = '\n'.join((aria_label, li.text.strip()))
    vals = [{'aria_label': aria_label,
             'carousel_options': carousel_options,
             'carousel_details': carousel_details}]
    return vals

# parsing tab navigation template


def tab_navigation(vn_tag):
    aria_label = vn_tag.find_all(
        "div", {"class": "know-tab-nav-widget-header"})[0].text.strip()
    corosel_pattern = re.compile('data-a-carousel-options=\'({.*})\'')
    carousel_options = re.findall(corosel_pattern, str(vn_tag))[0]
    carousel_details = []
    container = vn_tag.find("ol", {"class": "a-carousel"})
    for li in container.find_all('li', recursive=False):
        uuid = li.findChild("div")['data-uuid']
        if li.find_all("div", {"class": "s-card-container"}):
            carosuel_data = parse_search_results(li)
            carosuel_data[0]["uuid"] = uuid
            carousel_details.append(carosuel_data[0])
        else:
            aria_label = '\n'.join((aria_label, li.text.strip()))
    vals = [{'aria_label': aria_label,
             'carousel_options': carousel_options,
             'carousel_details': carousel_details}]
    return vals

# prasing fucntions dictionary
parsing_func_dict = {"SEARCH_RESULTS": parse_search_results, "VISUAL_NAVIGATION": parse_visual_navigation,
                     "FEATURED_ASINS_LIST": featured_asins_list, "SHOPPING_ADVISER": shopping_adviser,
                     "TAB_NAVIGATION": tab_navigation, "CARDS": cards}
# final parsing logic

def parsing_logic(soup, search_keyword):
    rid_pattern = re.compile('\"requestId\":\"(.*?)\"')
    request_id = re.findall(rid_pattern, str(soup))[0]
    pattern = re.compile('data-index=(\".*?\")')
    indexes = re.findall(pattern, str(soup))
    indexes = ','.join([i.replace('"', '') for i in indexes])
    indexes = indexes.split(",")

    widgets_data = []
    for widget_indx, i in enumerate(indexes, start=1):
        if i:
            result = soup.find_all("div", {"data-index": i})[0]
            # print(result)

            row = result

            # if upper slot is blank then div else span
            if soup.find_all("div", {"class": "slot=UPPER"}):
                tag = "div"
            else:
                tag = "span"

            # widget_id
            for x in row.find_all(tag, {"class": "slot=MAIN"})[0]['class']:
                if "widgetId=" in x:
                    widgetId = x.split("=")[1]
            # template_id
            for x in row.find_all(tag, {"class": "slot=MAIN"})[0]['class']:
                if "template=" in x:
                    template = x.split("=")[1]

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

    # conditionally assign view based on number of widgets
    if len(widgets_data) > 35:
        view = 'Grid view'
    else:
        view = 'List view'

    # export the scrapping Json results to a text file
    jsondata = {}
    search = {}
    content = {}
    search['query'] = search_keyword
    search['url'] = "https://www.amazon.com/s?k=" + search_keyword
    search['request_id'] = request_id
    search['search_results_view'] = view
    content['widgets'] = widgets_data

    jsondata['search'] = search
    jsondata['content'] = content

    with open('/Users/vekoppula/work/' + re.sub(r"\s+", "", search_keyword) + '.json', 'w') as outfile:
        json.dump(jsondata, outfile)
    return jsondata
