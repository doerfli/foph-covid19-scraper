from helper import extractIdx
import csv
import os

def processCases():
    data = extract_case_data()
    data = extract_hosp_data(data)
    write_cases_csv(data)


def extract_case_data():
    data = {}
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name == "COVID19Cases_geoRegion.csv"):
            print(name)
            data = parse_cases("%s/%s" % (base_dir, name), data)
        if (name == "COVID19Death_geoRegion.csv"):
            print(name)
            data = parse_death("%s/%s" % (base_dir, name), data)
    return data

def extract_hosp_data(data):
    base_dir = "./dataset/data"
    for name in os.listdir(base_dir):
        # print (name)
        if (name == "COVID19HospCapacity_geoRegion.csv"):
            print(name)
            data = parse_hosp("%s/%s" % (base_dir, name), data)
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
            data[canton][date] = { "total": 0, "current_hosp": 0, "current_icu": 0, "death": 0 }
        data[canton][date]["total"] = total
    return data

def parse_death(file, data):
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
            data[canton][date] = { "total": 0, "current_hosp": 0, "current_icu": 0, "death": 0 }
        data[canton][date]["death"] = total
    return data

def parse_hosp(file, data):
    idxGeoRegion = 0
    idxDate = 0
    idxCurrIcu = 0
    idxCurrHosp = 0
    csvreader = csv.reader(open(file, "r"), delimiter=',', quotechar='"')
    for row in csvreader:
        if row[0] == "date":
            idxGeoRegion, idxDate, idxCurrIcu, idxCurrHosp = extractIdx(row, 'geoRegion', 'date', 'ICU_Covid19Patients', 'Total_Covid19Patients')
            continue
        canton = row[idxGeoRegion]
        date = row[idxDate]
        currHosp = row[idxCurrHosp]
        currIcu = row[idxCurrIcu]
        if canton not in data:
            data[canton] = {}
        if date not in data[canton]:
            data[canton][date] = { "total": 0, "current_hosp": 0, "current_icu": 0, "death": 0 }
        data[canton][date]["current_hosp"] = currHosp
        data[canton][date]["current_icu"] = currIcu
    return data

def write_cases_csv(data):
    if not os.path.exists("cases"):
        os.mkdir("cases")
    totalcsvrows = []
    for canton in data:
        cdata = data[canton]
        with open("cases/cases_%s.csv" % canton, 'w', newline='') as csvfile:
            totalcsvrows = write_canton_csv(totalcsvrows, csvfile, canton, cdata)

    with open("cases/cases_total.csv", 'w', newline='') as totalcsvfile:
        totalcsvwriter = csv.writer(totalcsvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        totalcsvwriter.writerow(["date","time","abbreviation_canton_and_fl","ncumul_tested","ncumul_conf","new_hosp","current_hosp","current_icu","current_vent","ncumul_released","ncumul_deceased","source","current_isolated","current_quarantined","current_quarantined_riskareatravel","current_quarantined_total","ncumul_ICF"])
        totalcsvrows.sort(key=extract_date)
        for row in totalcsvrows:
            totalcsvwriter.writerow(row)

def extract_date(row):
    return row[0]

def write_canton_csv(totalcsvrows, csvfile, canton, cdata): 
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["date","time","abbreviation_canton_and_fl","ncumul_tested","ncumul_conf","new_hosp","current_hosp","current_icu","current_vent","ncumul_released","ncumul_deceased","source","current_isolated","current_quarantined","current_quarantined_riskareatravel","current_quarantined_total","ncumul_ICF"])
    for date in sorted(cdata):
        print("writing cases data for %s" % date)
        datasetDay = cdata[date]
        # print(datasetDay)
        csvrow = [
            date,
            "", #time
            canton, #abbreviation_canton_and_fl
            "", #ncumul_tested"
            datasetDay["total"], #"ncumul_conf"
            "", #new_hosp",
            datasetDay["current_hosp"], #"current_hosp",
            datasetDay["current_icu"], #"current_icu",
            "", #"current_vent",
            "", #"ncumul_released",
            datasetDay["death"], #"ncumul_deceased",
            "https://www.covid19.admin.ch/en/overview", #source",
            "", #"current_isolated",
            "", #"current_quarantined",
            "", #"current_quarantined_riskareatravel",
            "", #"current_quarantined_total",
            "", #"ncumul_ICF"]
        ]
        csvwriter.writerow(csvrow)
        totalcsvrows.append(csvrow)
    return totalcsvrows