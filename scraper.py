from urllib.request import urlopen
import re
import zipfile
from io import BytesIO
import csv
from io import TextIOWrapper

prefix = "https://www.covid19.admin.ch"
overview_src = urlopen("%s/en/overview" % prefix).read().decode('utf-8')
prog = re.compile("href=\"(/api/data/(.+)/sources-csv.zip)\"")
match = prog.search(overview_src)
# print(match)
# print(match.group(1))
data_url = "%s%s" % (prefix, match.group(1))
print("data_url: %s" % data_url)

vacc_data = {}

filebytes = BytesIO(urlopen(data_url).read())
fophdatazip = zipfile.ZipFile(filebytes)
for name in fophdatazip.namelist():
    if (name in ["data/COVID19FullyVaccPersons.csv", "data/COVID19VaccDosesAdministered.csv", "data/COVID19VaccDosesDelivered.csv"]):
        # print(name)
        # for line in fophdatazip.open(name).readlines():
        #     print(line)
        csvreader = csv.reader(TextIOWrapper(fophdatazip.open(name), 'utf-8'), delimiter=',', quotechar='"')
        for row in csvreader:
            if row[0] == "geoRegion":
                continue
            # print(', '.join(row))
            canton = row[0]
            date = row[1]
            total = row[3]
            per100 = row[4]
            dtype = row[5]
            if date not in vacc_data:
                vacc_data[date] = {}
            if canton not in vacc_data[date]:
                vacc_data[date][canton] = {}
            if dtype == "COVID19VaccDosesDelivered":
                vacc_data[date][canton]["deliveredTotal"] = total
                vacc_data[date][canton]["deliveredPer100"] = per100
            elif dtype == "COVID19VaccDosesAdministered":
                vacc_data[date][canton]["administeredTotal"] = total
                vacc_data[date][canton]["administeredPer100"] = per100
            elif dtype == "COVID19FullyVaccPersons":
                vacc_data[date][canton]["fullyVaccTotal"] = total
                vacc_data[date][canton]["fullyVaccPer100"] = per100

# print(vacc_data)

with open('vacc_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(["date", "canton", "deliveredTotal", "deliveredPer100", "administeredTotal", "administeredPer100", "fullyVaccinatedTotal", "fullyVaccinatedPer100"])
    for date in sorted(vacc_data):
        print("writing data for %s" % date)
        for canton in sorted(vacc_data[date]):
            data = vacc_data[date][canton]
            # print(data)
            dt = data["deliveredTotal"] if ("deliveredTotal" in data) else ""
            dp = data["deliveredPer100"] if ("deliveredPer100" in data) else ""
            at = data["administeredTotal"] if ("administeredTotal" in data) else ""
            ap = data["administeredPer100"] if ("administeredPer100" in data) else ""
            ft = data["fullyVaccTotal"] if ("fullyVaccTotal" in data) else ""
            fp = data["fullyVaccPer100"] if ("fullyVaccPer100" in data) else ""
            csvwriter.writerow([date, canton, dt, dp, at, ap, ft, fp])
