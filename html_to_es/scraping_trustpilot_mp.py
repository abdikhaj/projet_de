import requests, re, os, json
from custom_vars import vars
from tqdm import tqdm
from multiprocessing import Pool

# steps:
# 1- create all categories files
# 2- create companies files from the 17 default categories
# 3- create reviews files from the 17 default categories
# 4- third create a script to update a company if the company is not in the default companies


# create function to do the multiprocessing
def create_company_bulk_format(url):
    m = re.search('categories/([a-z_]+)\?page', url)
    n = re.search('page=(\d+)', url)
    if m:
        cat_name = m.group(1)
    if n:
        num_page = n.group(1)
    doc_name = cat_name + "_" + num_page

    html_respComp = requests.get(url=url)
    if html_respComp.status_code == 200:
        html_substr_comp = re.findall('"businesses"\:\[\{"businessUnitId".+\}\]\}\]\,"totalPages"', html_respComp.text)
        return r'{"create":{"_index":"comp_1","_id":"' + '{doc_name}"}}\n'.format(doc_name=doc_name) + '{' + html_substr_comp[0][:-13] + '}\n'




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


# delete the company file if exists
json_name = "companies_default"
if os.path.exists("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es"))):
  os.remove("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")))

# append the company file
html_all_comp = ""
for cat_name in tqdm(list_cat):
    
    # get the last num html page to loop on page
    urlCompLast = 'https://fr.trustpilot.com/categories/{cat_name}'.format(cat_name=cat_name)
    html_respCompLast = requests.get(url=urlCompLast)
    m = re.search('"totalPages"\:(\d+)\,"perPage"', html_respCompLast.text)
    if m:
        html_last_num_page = int(m.group(1))

    list_url_pool = ['https://fr.trustpilot.com/categories/{cat_name}?page='.format(cat_name=cat_name) + str(n) for n in range(1, html_last_num_page+1)]
    
    # loop on page with multiprocessing
    res = ""
    with Pool() as pool:
        # call the same function with different data in parallel
        for html_comp in pool.imap(create_company_bulk_format, list_url_pool):
            # report the value to show progress
            html_all_comp += html_comp

with open("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")), "a", encoding='utf-8') as file:
    file.write(html_all_comp)
