import requests
import re

# list urls
urlComp = 'https://fr.trustpilot.com/categories/hotels?page=1'
urlCat = 'https://fr.trustpilot.com/categories'
urlRev = 'https://fr.trustpilot.com/review/grandluxuryhotels.com'

# Get the page through get() method
html_respComp = requests.get(url=urlComp)
html_respCat = requests.get(url=urlCat)
html_respRev = requests.get(url=urlRev)

# select only the data we need
html_substr_comp = re.findall('"businesses"\:\[\{"businessUnitId".+\}\]\}\]\,"totalPages"', html_respComp.text)
html_substr_cat = re.findall('"subCategories"\:\{.+\]\}\]\}\,"languages"', html_respCat.text)
html_substr_rev1 = re.findall('"reviews"\:.+\}\]\,"products"', html_respRev.text)[0]
html_substr_rev = re.findall('"businessUnit"\:\{"id"\:"\w+"', html_respRev.text)[0] + '},' + html_substr_rev1

# transform to json
html_comp = '{"create":{"_index":"companies_1","_id":"1"}}\n' + '{' + html_substr_comp[0][:-13] + '}\n'
html_cat = '{"create":{"_index":"cat_1","_id":"1"}}\n' +'{' + html_substr_cat[0][:-12] + '}\n'
html_rev = '{"create":{"_index":"rev_1","_id":"1"}}\n' +'{' + html_substr_rev[:-11] + '}\n'


# create json_file
with open("categories.json", "w", encoding='utf-8') as file:
    file.write(html_cat)
with open("hotel_1.json", "w", encoding='utf-8') as file:
    file.write(html_comp)
with open("reviews_1.json", "w", encoding='utf-8') as file:
    file.write(html_rev)