import requests
import re
from custom_vars import vars
import os
from tqdm import tqdm

# steps:
# 1- create all categories files
# 2- create companies files from the 17 default categories
# 3- create reviews files from the 17 default categories
# 4- third create a script to update a company if the company is not in the default companies



# create all categories 
urlCat = 'https://fr.trustpilot.com/categories'
html_respCat = requests.get(url=urlCat)
html_substr_cat = re.findall('"subCategories"\:\{.+\]\}\]\}\,"languages"', html_respCat.text)
html_cat = '{"create":{"_index":"cat_1","_id":"1"}}\n' +'{' + html_substr_cat[0][:-12] + '}\n'
with open("{file_path}/categories.json".format(file_path=vars("file_path_push_to_es")), "w", encoding='utf-8') as file:
    file.write(html_cat)

# create companies files from the 17 default categories
json_name = "companies_default"

# delete the comapny file if exsts
if os.path.exists("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es"))):
  os.remove("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")))
# append the company file

for cat_name in tqdm(vars("default_category_name")):
    for num_page in tqdm(range(1,50), leave=False):
        doc_name = cat_name + "_" + str(num_page)
        urlComp = 'https://fr.trustpilot.com/categories/{cat_name}?page={num_page}'.format(cat_name=cat_name, num_page=num_page)
        html_respComp = requests.get(url=urlComp)
        if html_respComp.status_code == 200:
            html_substr_comp = re.findall('"businesses"\:\[\{"businessUnitId".+\}\]\}\]\,"totalPages"', html_respComp.text)
            html_comp = r'{"create":{"_index":"comp_1","_id":"' + '{doc_name}"}}\n'.format(doc_name=doc_name) + '{' + html_substr_comp[0][:-13] + '}\n'
            with open("{file_path}/{json_name}.json".format(json_name=json_name, file_path=vars("file_path_push_to_es")), "a", encoding='utf-8') as file:
                file.write(html_comp)
        else:
            break


"""
urlRev = 'https://fr.trustpilot.com/review/grandluxuryhotels.com'
html_respRev = requests.get(url=urlRev)
html_substr_rev1 = re.findall('"reviews"\:.+\}\]\,"products"', html_respRev.text)[0]
html_substr_rev = re.findall('"businessUnit"\:\{"id"\:"\w+"', html_respRev.text)[0] + '},' + html_substr_rev1
html_rev = '{"create":{"_index":"rev_1","_id":"1"}}\n' +'{' + html_substr_rev[:-11] + '}\n'

with open("{file_path}/reviews_1.json".format(file_path=vars("file_path_push_to_es")), "w", encoding='utf-8') as file:
    file.write(html_rev)
"""