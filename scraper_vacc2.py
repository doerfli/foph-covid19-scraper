import csv
import os
from helper import extractIdx

def processVaccData2():
    vacc_data = extractVaccData()
    # print(vacc_data)
    writeVaccCsv(vacc_data)

def extractVaccData():
    vacc_data = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name in ["COVID19VaccPersons_v2.csv"]):
            print(name)
            vacc_data = parseVaccPersons("%s/%s" % (base_dir, name), vacc_data)
    return vacc_data

def parseVaccPersons(file, vacc_data):
    idxGeoRegion = 0
    idxDate = 0
    idxSumTotal = 0
    idxPer100PersonsTotal = 0
    idxType = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "date": # skip header line
            idxGeoRegion, idxDate, idxSumTotal, idxPer100PersonsTotal, idxType, idxAgeGroup = extractIdx(row, 'geoRegion', 'date', 'sumTotal', 'per100PersonsTotal', 'type', 'age_group')
            continue
        # print(', '.join(row))
        date = row[idxDate]
        canton = row[idxGeoRegion]
        if canton in ["all", "neighboring_chfl", "unknown"]:
            continue
        total = row[idxSumTotal]
        per100 = row[idxPer100PersonsTotal]
        dtype = row[idxType]
        ageGroup = row[idxAgeGroup]
        if ageGroup != "total_population":
          continue
        if date not in vacc_data:
            vacc_data[date] = {}
        if canton not in vacc_data[date]:
            vacc_data[date][canton] = {}
        if dtype == "COVID19AtLeastOneDosePersons":
            vacc_data[date][canton]["atLeastOneDoseTotal"] = total
            vacc_data[date][canton]["atLeastOneDosePer100"] = per100
        elif dtype == "COVID19PartiallyVaccPersons":
            vacc_data[date][canton]["partiallyVaccTotal"] = total
            vacc_data[date][canton]["partiallyVaccPer100"] = per100
        elif dtype == "COVID19FullyVaccPersons":
            vacc_data[date][canton]["fullyVaccTotal"] = total
            vacc_data[date][canton]["fullyVaccPer100"] = per100
    return vacc_data

def writeVaccCsv(vacc_data):
    with open('vacc_data2.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["date", "canton", "atLeastOneDoseTotal", "atLeastOneDosePer100", "partiallyVaccTotal", "partiallyVaccPer100", "fullyVaccinatedTotal", "fullyVaccinatedPer100"])
        for date in sorted(vacc_data):
            print("writing vacc data for %s" % date)
            for canton in sorted(vacc_data[date]):
                data = vacc_data[date][canton]
                # print(data)
                lt = data["atLeastOneDoseTotal"] if ("atLeastOneDoseTotal" in data) else "0"
                lp = data["atLeastOneDosePer100"] if ("atLeastOneDosePer100" in data) else "0"
                pt = data["partiallyVaccTotal"] if ("partiallyVaccTotal" in data) else "0"
                pp = data["partiallyVaccPer100"] if ("partiallyVaccPer100" in data) else "0"
                ft = data["fullyVaccTotal"] if ("fullyVaccTotal" in data) else "0"
                fp = data["fullyVaccPer100"] if ("fullyVaccPer100" in data) else "0"
                csvwriter.writerow([date, canton, lt, lp, pt, pp, ft, fp])
