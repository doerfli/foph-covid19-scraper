import csv
import os
from helper import extractIdx

def processVaccData():
    vacc_data = extractVaccData()
    # print(vacc_data)
    writeVaccCsv(vacc_data)

def extractVaccData():
    vacc_data = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name == "COVID19VaccDosesDelivered.csv"):
            print(name)
            vacc_data = parseDelivered("%s/%s" % (base_dir, name), vacc_data)
        elif (name in ["COVID19VaccDosesAdministered.csv"]):
            print(name)
            vacc_data = parseAdministered("%s/%s" % (base_dir, name), vacc_data)
        elif (name in ["COVID19VaccPersons_v2.csv"]):
            print(name)
            vacc_data = parseVaccPersons("%s/%s" % (base_dir, name), vacc_data)
    return vacc_data

def parseDelivered(file, vacc_data):
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    idxGeoRegion = 0
    idxDate = 0
    idxSumTotal = 0
    idxPer100PersonsTotal = 0
    idxType = 0
    for row in csvreader:
        if row[0] == "geoRegion":
            idxGeoRegion, idxDate, idxSumTotal, idxPer100PersonsTotal, idxType = extractIdx(row, 'geoRegion', 'date', 'sumTotal', 'per100PersonsTotal', 'type')
            continue
        # print(', '.join(row))
        date = row[idxDate]
        canton = row[idxGeoRegion]
        if canton in ["all", "neighboring_chfl", "unknown"]:
            continue
        total = row[idxSumTotal]
        per100 = row[idxPer100PersonsTotal]
        type = row[idxType]
        if date not in vacc_data:
            vacc_data[date] = {}
        if canton not in vacc_data[date]:
            vacc_data[date][canton] = {}
        if type == "COVID19VaccDosesDelivered":
            vacc_data[date][canton]["deliveredTotal"] = total
            vacc_data[date][canton]["deliveredPer100"] = per100
        elif type == "COVID19VaccDosesReceived":
            vacc_data[date][canton]["receivedTotal"] = total
            vacc_data[date][canton]["receivedPer100"] = per100
    return vacc_data

def parseAdministered(file, vacc_data):
    idxGeoRegion = 0
    idxDate = 0
    idxSumTotal = 0
    idxPer100PersonsTotal = 0
    idxType = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "date": # skip header line
            idxGeoRegion, idxDate, idxSumTotal, idxPer100PersonsTotal, idxType = extractIdx(row, 'geoRegion', 'date', 'sumTotal', 'per100PersonsTotal', 'type')
            continue
        # print(', '.join(row))
        date = row[idxDate]
        canton = row[idxGeoRegion]
        if canton in ["all", "neighboring_chfl", "unknown"]:
            continue
        total = row[idxSumTotal]
        per100 = row[idxPer100PersonsTotal]
        dtype = row[idxType]
        if date not in vacc_data:
            vacc_data[date] = {}
        if canton not in vacc_data[date]:
            vacc_data[date][canton] = {}
        if dtype == "COVID19VaccDosesAdministered":
            vacc_data[date][canton]["administeredTotal"] = total
            vacc_data[date][canton]["administeredPer100"] = per100
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
        if dtype == "COVID19FullyVaccPersons":
            vacc_data[date][canton]["fullyVaccTotal"] = total
            vacc_data[date][canton]["fullyVaccPer100"] = per100
    return vacc_data

def writeVaccCsv(vacc_data):
    with open('vacc_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["date", "canton", "deliveredTotal", "deliveredPer100", "administeredTotal", "administeredPer100", "fullyVaccinatedTotal", "fullyVaccinatedPer100", "receivedTotal", "receivedPer100"])
        for date in sorted(vacc_data):
            print("writing vacc data for %s" % date)
            for canton in sorted(vacc_data[date]):
                data = vacc_data[date][canton]
                # print(data)
                dt = data["deliveredTotal"] if ("deliveredTotal" in data) else "0"
                dp = data["deliveredPer100"] if ("deliveredPer100" in data) else "0"
                at = data["administeredTotal"] if ("administeredTotal" in data) else "0"
                ap = data["administeredPer100"] if ("administeredPer100" in data) else "0"
                ft = data["fullyVaccTotal"] if ("fullyVaccTotal" in data) else "0"
                fp = data["fullyVaccPer100"] if ("fullyVaccPer100" in data) else "0"
                rt = data["receivedTotal"] if ("receivedTotal" in data) else "0"
                rp = data["receivedPer100"] if ("receivedPer100" in data) else "0"
                csvwriter.writerow([date, canton, dt, dp, at, ap, ft, fp, rt, rp])
