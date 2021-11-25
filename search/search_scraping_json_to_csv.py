# Import Module
import os
import json
import pandas as pd
import regex as re


def flatten_results_dic(data, search_keyword):
    keys = ['request_id', 'query', 'url', 'search_results_view', 'widget_indx','widgetId', 'template', 'item_id', 'component_type', 'title', 'price', 'star_rating', 'prime_label', 'rating_size',
            'badge', 'more_buying_choice', 'product_specs', 'uuid', 'carousel_options', 'aria_label']
    df = dict([(key, []) for key in keys])
    for i in range(len(data['content']['widgets'])):
        if "carousel_product_names" in data['content']['widgets'][i].keys():
            df['item_id'].append("")
            df['component_type'].append("")
            df['title'].append("")
            df['price'].append("")
            df['star_rating'].append("")
            df['prime_label'].append("")
            df['rating_size'].append("")
            df['badge'].append("")
            df['more_buying_choice'].append("")
            df['product_specs'].append(
                data['content']['widgets'][i]['carousel_product_names'])
            df['uuid'].append("")
            df['request_id'].append(data['search']['request_id'])
            df['query'].append(data['search']['query'])
            df['url'].append(data['search']['url'])
            df['search_results_view'].append(
                data['search']['search_results_view'])
            df['widget_indx'].append(data['content']['widgets'][i]['widget_indx'])
            df['widgetId'].append(data['content']['widgets'][i]['widgetId'])
            df['template'].append(data['content']['widgets'][i]['template'])
            df['carousel_options'].append(
                data['content']['widgets'][i]['carousel_options'])
            df['aria_label'].append(
                data['content']['widgets'][i]['aria_label'])

        elif "carousel_details" in data['content']['widgets'][i].keys():
            for c in range(len(data['content']['widgets'][i]['carousel_details'])):
                df['item_id'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['item_id'])
                df['component_type'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['component_type'])
                df['title'].append(data['content']['widgets']
                                   [i]['carousel_details'][c]['title'])
                df['price'].append(data['content']['widgets']
                                   [i]['carousel_details'][c]['price'])
                df['star_rating'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['star_rating'])
                df['prime_label'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['prime_label'])
                df['rating_size'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['rating_size'])
                df['badge'].append(data['content']['widgets']
                                   [i]['carousel_details'][c]['badge'])
                df['more_buying_choice'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['more_buying_choice'])
                df['product_specs'].append(
                    data['content']['widgets'][i]['carousel_details'][c]['product_specs'])
                df['uuid'].append(data['content']['widgets']
                                  [i]['carousel_details'][c]['uuid'])
                df['request_id'].append(data['search']['request_id'])
                df['query'].append(data['search']['query'])
                df['url'].append(data['search']['url'])
                df['search_results_view'].append(
                    data['search']['search_results_view'])
                df['widget_indx'].append(
                    data['content']['widgets'][i]['widget_indx'])
                df['widgetId'].append(
                    data['content']['widgets'][i]['widgetId'])
                df['template'].append(
                    data['content']['widgets'][i]['template'])
                df['carousel_options'].append(
                    data['content']['widgets'][i]['carousel_options'])
                df['aria_label'].append(
                    data['content']['widgets'][i]['aria_label'])

        else:
            try:
                df['item_id'].append(
                    data['content']['widgets'][i]['item_id'])
                df['component_type'].append(
                    data['content']['widgets'][i]['component_type'])
                df['title'].append(data['content']['widgets'][i]['title'])
                df['price'].append(data['content']['widgets'][i]['price'])
                df['star_rating'].append(
                    data['content']['widgets'][i]['star_rating'])
                df['prime_label'].append(
                    data['content']['widgets'][i]['prime_label'])
                df['rating_size'].append(
                    data['content']['widgets'][i]['rating_size'])
                df['badge'].append(data['content']['widgets'][i]['badge'])
                df['more_buying_choice'].append(
                    data['content']['widgets'][i]['more_buying_choice'])
                df['product_specs'].append(
                    data['content']['widgets'][i]['product_specs'])
                df['uuid'].append("")
                df['request_id'].append(data['search']['request_id'])
                df['query'].append(data['search']['query'])
                df['url'].append(data['search']['url'])
                df['search_results_view'].append(
                    data['search']['search_results_view'])
                df['widget_indx'].append(
                    data['content']['widgets'][i]['widget_indx'])
                df['widgetId'].append(
                    data['content']['widgets'][i]['widgetId'])
                df['template'].append(
                    data['content']['widgets'][i]['template'])
                df['carousel_options'].append("")
                df['aria_label'].append("")
            except KeyError:
                df['item_id'].append("")
                df['component_type'].append("")
                df['title'].append("")
                df['price'].append("")
                df['star_rating'].append("")
                df['prime_label'].append("")
                df['rating_size'].append("")
                df['badge'].append("")
                df['more_buying_choice'].append("")
                df['product_specs'].append("")
                df['uuid'].append("")
                df['request_id'].append(data['search']['request_id'])
                df['query'].append(data['search']['query'])
                df['url'].append(data['search']['url'])
                df['search_results_view'].append(
                    data['search']['search_results_view'])
                df['widget_indx'].append(
                    data['content']['widgets'][i]['widget_indx'])
                df['widgetId'].append(
                    data['content']['widgets'][i]['widgetId'])
                df['template'].append(
                    data['content']['widgets'][i]['template'])
                df['carousel_options'].append("")
                df['aria_label'].append("")
    pd.DataFrame(df).to_csv('/Users/vekoppula/work/' + re.sub(r"\s+",
                                                              "", search_keyword) + '.csv', header=True, index=False)
