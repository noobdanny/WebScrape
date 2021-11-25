# Import Module
import os
import json
import pandas as pd
import regex as re


def flatten_results_dic(data, id):
    keys = ['request_id', 'seed_item_id', 'seed_item_title', 'seed_item_price', 'module_index', 'module_title', 'module_content_type', 'set_size', 'carousel_name',
            'item_index', 'item_id', 'title', 'price', 'star_rating', 'prime_label', 'rating_size']
    df = dict([(key, []) for key in keys])
    for i in range(len(data['module_container'])):
        for j in range(len(data['module_container'][i]['items_container'])):
            df['request_id'].append(data['request_id'])
            df['seed_item_id'].append(data['seed_item_id'])
            df['seed_item_title'].append(data['seed_item_title'])
            df['seed_item_price'].append(data['seed_item_price'])
            df['module_index'].append(
                data['module_container'][i]['module_index'])
            df['module_title'].append(
                data['module_container'][i]['module_title'])
            df['module_content_type'].append(
                data['module_container'][i]['module_content_type'])
            df['set_size'].append(data['module_container']
                                  [i]['carousel_options']['set_size'])
            df['carousel_name'].append(
                data['module_container'][i]['carousel_options']['name'])
            df['item_index'].append(
                data['module_container'][i]['items_container'][j]['item_index'])
            df['item_id'].append(data['module_container']
                                 [i]['items_container'][j]['item_id'])
            df['title'].append(data['module_container'][i]
                               ['items_container'][j]['title'])
            df['price'].append(data['module_container'][i]
                               ['items_container'][j]['price'])
            df['star_rating'].append(
                data['module_container'][i]['items_container'][j]['star_rating'])
            df['prime_label'].append(
                data['module_container'][i]['items_container'][j]['prime_label'])
            df['rating_size'].append(
                data['module_container'][i]['items_container'][j]['rating_size'])

    pd.DataFrame(df).to_csv('/Users/vekoppula/work/Merch/' + re.sub(r"\s+",
                                                                    "", id) + '.csv', header=True, index=False)
