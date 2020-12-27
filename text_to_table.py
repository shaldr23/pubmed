# %%
import pandas as pd
import re

MEDLINE_TEXT_FILE = './data/output/results.medline'


def processrecord(record: str,
                  fields=['PMID', 'DP', 'TI', 'BTI',
                          'AB', 'PT', 'OT']) -> 'pd.Series':
    """
    One record into Series
    """
    record = record.strip()
    record = record.replace('\n' + ' '*6, ' ')
    result = pd.Series()
    for line in record.split('\n'):
        field = line[:4].strip()
        value = line[6:]
        if field in fields:
            if field not in result.index:
                result[field] = value
            else:
                if type(result[field]) != list:
                    result[field] = [result[field]]
                result[field].append(value)
    return result


records_list = []
with open(MEDLINE_TEXT_FILE) as mtf:
    record = ''
    for line in mtf:
        record += line
        if line == '\n' and record != '\n':
            records_list.append(processrecord(record))
            record = ''
if record:
    records_list.append(processrecord(record))  # catch last record

frame = pd.DataFrame(records_list)
