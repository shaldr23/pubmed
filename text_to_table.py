# %%
import pandas as pd
import re

MEDLINE_TEXT_FILE = '.data/output/results.medline'


def processrecord(record: str,
                  exclude_fields=['AU', 'FAU', 'AD']) -> 'pd.Series':
    """
    One record into Series
    """
    record = record.strip()
    result = pd.Series()
    re = r'^\w{2,4}'  # to correct
    for line in record:
        field = record[:4]
        value = record[7:]


record = ''
with open(MEDLINE_TEXT_FILE) as mtf:
    line = mtf.readline()
    record += line
    if line == '\n':
        processrecord(record)
