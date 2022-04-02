from helper import extractIdx
import csv
import os

def process_timestamps():
    data = extract_timestamp_data()
    write_csv(data)


def extract_timestamp_data():
    data = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name == "COVID19EvalTextDaily.csv"):
            print(name)
            data = parse_timestamps("%s/%s" % (base_dir, name), data)
    return data

def parse_timestamps(file, data):
    idxVariant = 0
    idxVersion = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "type":
            idxVariant, idxVersion = extractIdx(row, 'type_variant', 'version')
            continue
        variant = row[idxVariant][10:]
        timestamp = row[idxVersion]
        data[variant] = timestamp
    return data

def write_csv(data):
    print("Writing timetable to file...")
    with open('timestamps.csv', 'w') as csvfile:
        fieldnames = ['type', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in data.items():
            writer.writerow({'type': key, 'timestamp': value})   
            