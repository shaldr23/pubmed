# %%
import json
import requests

TERM = 'SARS-CoV-2 OR COVID-19'
with open('user_key.json') as key_file:
    user_data = json.load(key_file)

basic_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'
params = {'db': 'pubmed'}
params.update(user_data)
req = requests.get(basic_url, params=params)
