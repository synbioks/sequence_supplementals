import requests
import json
import pandas as pd

progress = True
all_pages = []

with open('igem_parts_list_sparql.txt', 'r') as f:
    query = f.read()


for i in range(0, 2000):

    if progress:  # print progress
        print(i)

    # replace placeholder in query_text with page number to get
    queryed = query.replace("REPLACE_HERE", str(i*10000))
    response = requests.post("https://synbiohub.org/sparql",
                             data={"query": queryed},
                             headers={"Accept": "application/json"})

    print(response.status_code)

    d = json.loads(response.text)
    one_page = pd.json_normalize(d['results']['bindings'])
    # add page data to all pages data
    all_pages.append(one_page)

    # if the page was no longer a full page stop loop
    if len(one_page) < 10000:
        break

# create pandas data frame containing all page information
all_pages = pd.concat(all_pages)
all_pages.to_csv('creation_dates.csv')
# print(all_pages, len(all_pages))
