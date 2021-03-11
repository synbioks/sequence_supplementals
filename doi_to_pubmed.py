#api guide: https://www.ncbi.nlm.nih.gov/pmc/tools/id-converter-api/
#converter gui: https://www.ncbi.nlm.nih.gov/pmc/pmctopmid/

import requests

#this only works if the article also has a pmcid
dois_seperated_by_commas = '10.1021/acssynbio.8b00430, 10.1021/acssynbio.9b00160'

url = f'https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/?ids={dois_seperated_by_commas}&versions=no&format=json'

r = requests.get(url)
print(r.json()['records'])