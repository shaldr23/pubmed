# %%
import json
import requests
import time


TIME_BETWEEN_REQUESTS = .15
TERM = 'SARS-CoV-2 OR COVID-19'
REQUEST_TRIES = 3
TIME_BETWEEN_TRIES = 5
RECORDS_COUNT = 1000  # How many records to obtain. If == False, obtain all
BATCH_SIZE = 100  # 'retmax' parameter, 10**4 is maximum
PRIMARY_OUTPUT_FILE = './output/results.medline'


search_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'
fetch_url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?'


def make_request(basic_url, params):
    """
    Make request (esearch or efetch).
    Makes several tries of a request if status code is not 200.
    Keeps request rate limitation.
    Returns request object.
    """
    params = params.copy()
    params.update(user_data)
    for i in range(REQUEST_TRIES):
        if time.time() - make_request.last_request_time < TIME_BETWEEN_REQUESTS:
            time.sleep(TIME_BETWEEN_REQUESTS)
        make_request.last_request_time = time.time()
        req = requests.get(basic_url, params=params)
        if req.status_code == 200:
            return req
            break
        else:
            print('Request attempt failed')
            time.sleep(TIME_BETWEEN_TRIES)
    raise ValueError('Wrong request results.')


make_request.last_request_time = 0

with open('user_key.json') as key_file:
    user_data = json.load(key_file)

# esearch
search_params = {'term': TERM,
                 'db': 'pubmed',
                 'retmode': 'json',
                 'usehistory': 'y'}
req = make_request(search_url, search_params)
search_result = req.json()['esearchresult']
webenv = search_result['webenv']
count = int(search_result['count'])
key = search_result['querykey']

# efetch
limit = RECORDS_COUNT if RECORDS_COUNT else count
with open(PRIMARY_OUTPUT_FILE, 'w') as output:
    for cycle, retstart in enumerate(range(0, limit, BATCH_SIZE), start=1):
        fetch_params = {'db': 'pubmed',
                        'WebEnv': webenv,
                        'query_key': key,
                        'retstart': retstart,
                        'retmax': BATCH_SIZE,
                        'rettype': 'medline'}
        data = make_request(fetch_url, fetch_params).text
        output.write(data)
        articles_count = data.count('\n\n') + 1
        print(f'Cycle № {cycle}, articles count: {articles_count}')

# %%
