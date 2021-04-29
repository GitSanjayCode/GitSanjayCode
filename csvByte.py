import requests
from contextlib import closing
import csv

url = "http://samplecsvs.s3.amazonaws.com/SalesJan2009.csv"

with closing(requests.get(url, stream=True)) as r:
    f = (line.decode('utf-8') for line in r.iter_lines())
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        print(row)
