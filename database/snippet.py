import csv

with open('../data/processed/cleaned_train.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    headers = next(reader)
    print(headers)

