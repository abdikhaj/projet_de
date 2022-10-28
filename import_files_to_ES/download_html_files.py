import xmltojson
import json
import requests
import html_to_json

url = 'https://fr.trustpilot.com/categories/hotels'

# Get the page through get() method
html_response = requests.get(url=url)
  
# create html file from the page saved
with open("hotel_1.html", "w") as html_file:
    html_file.write(html_response.text)
# convert html to json
with open("hotel_1.html", "r") as html_file:
    html = html_file.read()
    output_json = html_to_json.convert(html)
# create json file 
with open("hotel_1.json", "w") as file:
    json.dump(output_json, file)