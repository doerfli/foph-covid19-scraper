import csv
import os
from helper import extractIdx

def process_pop_data():
    data = extract_pop_data()
    #print(data)
    write_pop_csv(data)

def extract_pop_data():
    data = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name in ["COVID19VaccPersons_v2.csv"]):
            print(name)
            data = parsePersons("%s/%s" % (base_dir, name), data)
    return data

def parsePersons(file, data):
    idxGeoRegion = 0
    idxPop = 0
    idxAgeGroup = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "date": # skip header line
            idxGeoRegion, idxPop, idxAgeGroup = extractIdx(row, 'geoRegion', 'pop', 'age_group')
            continue
        # print(', '.join(row))
        if (row[idxAgeGroup] != 'total_population'):
            continue
        if not row[idxPop].isnumeric():
            continue
        canton = row[idxGeoRegion]
        pop = row[idxPop]
        data[canton] = pop
    return data

def write_pop_csv(data):
    with open('pop.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["canton", "pop"])
        for canton in sorted(data):
            print("writing pop data for %s" % canton)
            pop = data[canton]
            csvwriter.writerow([canton, pop])
