import csv

with open('data.csv', 'r', encoding='utf8') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row[1:5])
