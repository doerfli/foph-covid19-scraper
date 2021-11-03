from urllib.request import urlopen
import json
import re
import zipfile
import os.path
from scraper_vacc import processVaccData
from scraper_vacc2 import processVaccData2
from scraper_cases import processCases
from scraper_pop import process_pop_data

def main():
    download_data()
    process_pop_data()
    processVaccData()
    processVaccData2()
    processCases()

def download_data():
    if os.path.exists("./dataset.zip"):
        print("dataset.zip already exists. using existing file")
        return
    data_url = getDataUrl()
    print("data_url: %s" % data_url)
    
    with urlopen(data_url) as dl_file:
        with open("./dataset.zip", 'wb') as out_file:
            out_file.write(dl_file.read())
    z = zipfile.ZipFile("./dataset.zip")
    z.extractall("./dataset/")

def getDataUrl():
    context_json = json.loads(urlopen("https://www.covid19.admin.ch/api/data/context").read())
    return context_json['sources']['zip']['csv']


if __name__ == "__main__":
    # execute only if run as a script
    main()
