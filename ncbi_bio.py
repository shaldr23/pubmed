"""
Скрипт использует biopython
Скрипт оценивает динамику встречаемости статей с заданной тематикой.
Количества статей выравниваются на общее количество статей
в соответствующем году, а первый ненулевой показатель в ряду принимается за 1.
В папке должен быть файл 'user_key.json'.
В нем должны быть поля 'email', 'tool', а также 'api_key', полученное от ncbi.
api_key позволяет делать запросы с большей частотой.
"""
from Bio import Entrez
import numpy as np
import matplotlib.pyplot as plt
import json


def search(query, year):
    handle = Entrez.esearch(db="pubmed",
                            term=query,
                            mindate=year,
                            maxdate=year)
    result = Entrez.read(handle)
    handle.close()
    return result['Count']


with open('user_key.json') as key_file:
    user_data = json.load(key_file)
Entrez.email = user_data['email']
Entrez.api_key = user_data['api_key']
Entrez.tool = user_data['tool']

term = input('input query: \n')
values = []
all_articles_values = []
years = []
for i in range(2000, 2021):
    years.append(str(i))
    values.append(int(search(term, str(i))))
    all_articles_values.append(int(search('', str(i))))
values = np.array(values)/all_articles_values
not_null_index = np.where(values)[0][0]
values = values/values[not_null_index]
plt.bar(years, height=values)
plt.xlabel("год")
plt.title("Динамика встречаемости статей, связанных с " + term)
plt.show()
