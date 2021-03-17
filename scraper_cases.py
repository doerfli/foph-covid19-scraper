from helper import extractIdx
import csv
import os

def processCases():
    data = extract_case_data()
    write_cases_csv(data)


def extract_case_data():
    data = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name == "COVID19Cases_geoRegion.csv"):
            print(name)
            data = parse_cases("%s/%s" % (base_dir, name), data)
    return data

def parse_cases(file, data):
    idxGeoRegion = 0
    idxDatum = 0
    idxSumTotal = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "geoRegion":
            idxGeoRegion, idxDatum, idxSumTotal = extractIdx(row, 'geoRegion', 'datum', 'sumTotal')
            continue
        canton = row[idxGeoRegion]
        date = row[idxDatum]
        total = row[idxSumTotal]
        if canton not in data:
            data[canton] = {}
        if date not in data[canton]:
            data[canton][date] = {}
        data[canton][date]["total"] = total
    return data

def write_cases_csv(data):
    for canton in data:
        cdata = data[canton]
        with open("cases_%s.csv" % canton, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["date","time","abbreviation_canton_and_fl","ncumul_tested","ncumul_conf","new_hosp","current_hosp","current_icu","current_vent","ncumul_released","ncumul_deceased","source","current_isolated","current_quarantined","current_quarantined_riskareatravel","current_quarantined_total","ncumul_ICF"])
            for date in sorted(cdata):
                print("writing cases data for %s" % date)
                datasetDay = data[canton][date]
                # print(datasetDay)
                csvwriter.writerow([
                    date,
                    "", #time
                    canton, #abbreviation_canton_and_fl
                    "", #ncumul_tested"
                    datasetDay["total"], #"ncumul_conf"
                    "", #new_hosp",
                    "", #"current_hosp",
                    "", #"current_icu",
                    "", #"current_vent",
                    "", #"ncumul_released",
                    "", #"ncumul_deceased",
                    "https://www.covid19.admin.ch/en/overview", #source",
                    "", #"current_isolated",
                    "", #"current_quarantined",
                    "", #"current_quarantined_riskareatravel",
                    "", #"current_quarantined_total",
                    "", #"ncumul_ICF"]
                ])
