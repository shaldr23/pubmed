# %%
"""
Script to make a pandas DataFrame object
from a text file in MEDLINE format
"""
import pandas as pd
import re
import pickle

MEDLINE_TEXT_FILE = './data/output/results.medline'
SAVE_TABLE = './data/output/table.pickle'


def processrecord(record: str,
                  fields=['PMID', 'DP', 'TI', 'BTI',
                          'AB', 'PT', 'OT']) -> 'pd.Series':
    """
    Convert one record into pd.Series
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


def all_lists(value):
    """
    Convert all values into list in columns containing lists
    (used in pd.Series.apply method)
    """
    if type(value) == list:
        return value
    elif pd.isna(value):
        return []
    else:
        return [value]


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

# dates should contain at least month
good_dates = frame['DP'].apply(lambda x: bool(re.match(r'\d{4} \w{3}', x)))
frame = frame[good_dates]
frame['date'] = pd.to_datetime(frame['DP'], yearfirst=True, errors='coerce')
frame.dropna(subset=['date'], inplace=True)
frame['date_month'] = frame['date'].apply(lambda x: x.replace(day=1))
frame.reset_index(drop=True, inplace=True)
# columns containing lists should have all list values
for col in frame:
    if list in frame[col].apply(type).values:
        frame[col] = frame[col].apply(all_lists)

if SAVE_TABLE:
    with open(SAVE_TABLE, 'wb') as f:
        pickle.dump(frame, f)
