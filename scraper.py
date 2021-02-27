from urllib.request import urlopen
import re
import zipfile
from io import BytesIO
import csv
from io import TextIOWrapper


def main():
    data_url = getDataUrl()
    print("data_url: %s" % data_url)
    vacc_data = processZipStreamAndExtractData(data_url)
    print(vacc_data)
    writeCsv(vacc_data)

def getDataUrl():
    prefix = "https://www.covid19.admin.ch"
    overview_src = urlopen("%s/en/overview" % prefix).read().decode('utf-8')
    prog = re.compile("href=\"(/api/data/(.+)/sources-csv.zip)\"")
    match = prog.search(overview_src)
    # print(match)
    # print(match.group(1))
    return "%s%s" % (prefix, match.group(1))

def processZipStreamAndExtractData(data_url):
    vacc_data = {}
    filebytes = BytesIO(urlopen(data_url).read())
    fophdatazip = zipfile.ZipFile(filebytes)
    for name in fophdatazip.namelist():
        if (name == "data/COVID19VaccDosesDelivered.csv"):
            print(name)
            vacc_data = parseDelivered(fophdatazip, name, vacc_data)
        elif (name in ["data/COVID19FullyVaccPersons.csv", "data/COVID19VaccDosesAdministered.csv"]):
            print(name)
            vacc_data = parsePersons(fophdatazip, name, vacc_data)
    return vacc_data

def parseDelivered(fophdatazip, name, vacc_data):
    csvreader = csv.reader(TextIOWrapper(fophdatazip.open(name), 'utf-8'), delimiter=',', quotechar='"')
    idxGeoRegion = 0
    idxDate = 0
    idxSumTotal = 0
    idxPer100PersonsTotal = 0
    for row in csvreader:
        if row[0] == "geoRegion":
            idxGeoRegion, idxDate, idxSumTotal, idxPer100PersonsTotal = extractIdx(row, 'geoRegion', 'date', 'sumTotal', 'per100PersonsTotal')
            continue
        # print(', '.join(row))
        canton = row[idxGeoRegion]
        date = row[idxDate]
        total = row[idxSumTotal]
        per100 = row[idxPer100PersonsTotal]
        if date not in vacc_data:
            vacc_data[date] = {}
        if canton not in vacc_data[date]:
            vacc_data[date][canton] = {}
        vacc_data[date][canton]["deliveredTotal"] = total
        vacc_data[date][canton]["deliveredPer100"] = per100
    return vacc_data

def extractIdx(row, *idxNames):
    idxs = []
    for idx in idxNames:
        for i in range(len(row)):
            if row[i] == idx:
                idxs.append(i)
    return idxs

def parsePersons(fophdatazip, name, vacc_data):
    idxGeoRegion = 0
    idxDate = 0
    idxSumTotal = 0
    idxPer100PersonsTotal = 0
    idxType = 0
    csvreader = csv.reader(TextIOWrapper(fophdatazip.open(name), 'utf-8'), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "date": # skip header line
            idxGeoRegion, idxDate, idxSumTotal, idxPer100PersonsTotal, idxType = extractIdx(row, 'geoRegion', 'date', 'sumTotal', 'per100PersonsTotal', 'type')
            continue
        # print(', '.join(row))
        date = row[idxDate]
        canton = row[idxGeoRegion]
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
        elif dtype == "COVID19FullyVaccPersons":
            vacc_data[date][canton]["fullyVaccTotal"] = total
            vacc_data[date][canton]["fullyVaccPer100"] = per100
    return vacc_data

def writeCsv(vacc_data):
    with open('vacc_data.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(["date", "canton", "deliveredTotal", "deliveredPer100", "administeredTotal", "administeredPer100", "fullyVaccinatedTotal", "fullyVaccinatedPer100"])
        for date in sorted(vacc_data):
            print("writing data for %s" % date)
            for canton in sorted(vacc_data[date]):
                data = vacc_data[date][canton]
                # print(data)
                dt = data["deliveredTotal"] if ("deliveredTotal" in data) else "0"
                dp = data["deliveredPer100"] if ("deliveredPer100" in data) else "0"
                at = data["administeredTotal"] if ("administeredTotal" in data) else "0"
                ap = data["administeredPer100"] if ("administeredPer100" in data) else "0"
                ft = data["fullyVaccTotal"] if ("fullyVaccTotal" in data) else "0"
                fp = data["fullyVaccPer100"] if ("fullyVaccPer100" in data) else "0"
                csvwriter.writerow([date, canton, dt, dp, at, ap, ft, fp])


if __name__ == "__main__":
    # execute only if run as a script
    main()
