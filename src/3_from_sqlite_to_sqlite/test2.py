import requests

comp_name = "grandluxuryhotels.com"
urlRevLast = 'https://fr.trustpilot.com/review/{website}'.format(website=comp_name)
html_respRevLast = requests.get(url=urlRevLast)
with open("./src/3_from_sqlite_to_sqlite/res_rev", "w") as f:
    f.write(html_respRevLast.text)