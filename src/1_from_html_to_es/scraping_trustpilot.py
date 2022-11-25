#!/usr/bin/env python3

import requests, re, os, json
from custom_vars import vars
from tqdm import tqdm

# steps:
# 1- create all categories file -> categories.json
# 2- create  all companies file -> companies_default.json



# create the file categories.json in bulk Elasticsearch format
urlCat = 'https://fr.trustpilot.com/categories'
html_respCat = requests.get(url=urlCat)
html_substr_cat = re.findall('"subCategories"\:\{.+\]\}\]\}\,"languages"', html_respCat.text)
html_cat_data = '{' + html_substr_cat[0][:-12] + '}'
html_cat = '{"create":{"_index":"cat_1","_id":"1"}}\n' + str(html_cat_data) + '\n'
with open("{file_path}/categories.json".format(file_path=vars("file_path_push_to_es")), "w", encoding='utf-8') as file:
    file.write(html_cat)

# create a list with all the categories
list_cat = []
dict_cat = json.loads(html_cat_data)
for k_cat in dict_cat["subCategories"]:
    for l in dict_cat["subCategories"][k_cat]:
        list_cat.append(l["categoryId"])


# delete the company file if exsts
json_name = "companies_default"
if os.path.exists("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es"))):
  os.remove("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")))

# create companies file
html_all_comp = ""
for cat_name in tqdm(["hotels"]):
    
    # get the last num html page to loop on page
    urlCompLast = 'https://fr.trustpilot.com/categories/{cat_name}'.format(cat_name=cat_name)
    html_respCompLast = requests.get(url=urlCompLast)
    m = re.search('"totalPages"\:(\d+)\,"perPage"', html_respCompLast.text)
    if m:
        html_last_num_page = int(m.group(1))

    # loop on page
    for num_page in range(1, html_last_num_page+1):
        doc_name = cat_name + "_" + str(num_page)
        urlComp = 'https://fr.trustpilot.com/categories/{cat_name}?page={num_page}'.format(cat_name=cat_name, num_page=num_page)
        html_respComp = requests.get(url=urlComp)
        if html_respComp.status_code == 200:
            html_substr_comp = re.findall('"businesses"\:\[\{"businessUnitId".+\}\]\}\]\,"totalPages"', html_respComp.text)
            html_comp = r'{"create":{"_index":"comp_1","_id":"' + '{doc_name}"}}\n'.format(doc_name=doc_name) + '{' + html_substr_comp[0][:-13] + '}\n'
            html_all_comp += html_comp
        else:
            break

with open("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")), "a", encoding='utf-8') as file:
    file.write(html_all_comp)