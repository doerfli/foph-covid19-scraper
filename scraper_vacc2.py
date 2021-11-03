import csv
import os
from helper import extractIdx

def processVaccData2():
    vacc_data_total, vacc_data_twelveplus = extractVaccData()
    # print(vacc_data)
    writeVaccCsv(vacc_data_total, vacc_data_twelveplus)

def extractVaccData():
    vacc_data_total = {}
    vacc_data_twelveplus = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name in ["COVID19VaccPersons_v2.csv"]):
            print(name)
            vacc_data_total, vacc_data_twelveplus = parseVaccPersons("%s/%s" % (base_dir, name), vacc_data_total, vacc_data_twelveplus)
    return vacc_data_total, vacc_data_twelveplus

def parseVaccPersons(file, vacc_data_total, vacc_data_twelveplus):
    idxGeoRegion = 0
    idxDate = 0
    idxSumTotal = 0
    idxPer100PersonsTotal = 0
    idxType = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "date": # skip header line
            idxGeoRegion, idxDate, idxSumTotal, idxPer100PersonsTotal, idxType, idxAgeGroup, idxPop = extractIdx(row, 'geoRegion', 'date', 'sumTotal', 'per100PersonsTotal', 'type', 'age_group', 'pop')
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
        pop = row[idxPop]
        if ageGroup == "total_population":
            vacc_data_total = getVaccData(vacc_data_total, date, canton, pop, dtype, total, per100)
        elif ageGroup == "12+":
            vacc_data_twelveplus = getVaccData(vacc_data_twelveplus, date, canton, pop, dtype, total, per100)
    return vacc_data_total, vacc_data_twelveplus

def getVaccData(vacc_data, date, canton, pop, dtype, total, per100):
    if date not in vacc_data:
        vacc_data[date] = {}
    if canton not in vacc_data[date]:
        vacc_data[date][canton] = {}
    if "pop" not in vacc_data[date][canton]:
        vacc_data[date][canton]["pop"] = pop
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

def writeVaccCsv(vacc_data_total, vacc_data_twelveplus):
    if not os.path.exists("vacc_data"):
        os.mkdir("vacc_data")
    writeVaccCsvFile(vacc_data_total, 'vacc_data/vacc_data2_total.csv')
    writeVaccCsvFile(vacc_data_twelveplus, 'vacc_data/vacc_data2_twelveplus.csv')

def writeVaccCsvFile(vacc_data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["date", "canton", "pop", "atLeastOneDoseTotal", "atLeastOneDosePer100", "partiallyVaccTotal", "partiallyVaccPer100", "fullyVaccinatedTotal", "fullyVaccinatedPer100"])
        for date in sorted(vacc_data):
            print("writing vacc data for %s" % date)
            for canton in sorted(vacc_data[date]):
                data = vacc_data[date][canton]
                pop = data["pop"]
                # print(data)
                lt = data["atLeastOneDoseTotal"] if ("atLeastOneDoseTotal" in data) else "0"
                lp = data["atLeastOneDosePer100"] if ("atLeastOneDosePer100" in data) else "0"
                pt = data["partiallyVaccTotal"] if ("partiallyVaccTotal" in data) else "0"
                pp = data["partiallyVaccPer100"] if ("partiallyVaccPer100" in data) else "0"
                ft = data["fullyVaccTotal"] if ("fullyVaccTotal" in data) else "0"
                fp = data["fullyVaccPer100"] if ("fullyVaccPer100" in data) else "0"
                csvwriter.writerow([date, canton, pop, lt, lp, pt, pp, ft, fp])
