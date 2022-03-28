from urllib.request import urlopen
import json
import re
import zipfile
import os.path
import sys
from scraper_vacc import processVaccData
from scraper_vacc2 import processVaccData2
from scraper_cases import processCases
from scraper_pop import process_pop_data
from pathlib import Path
from checksum import calculate_filehash

def main():
    download_data()
    dataset_checksum = check_if_dataset_has_been_processed_before()
    process_pop_data()
    processVaccData()
    processVaccData2()
    processCases()
    update_dataset_checksum(dataset_checksum)

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

def check_if_dataset_has_been_processed_before():
    checksum = calculate_filehash("./dataset.zip")
    
    if not os.path.exists("./dataset.zip.latest.sha256"):
        return checksum

    checksum_of_last_run = ""
    with open("./dataset.zip.latest.sha256","r") as f:
        checksum_of_last_run = f.read()

    if checksum == checksum_of_last_run:
        print("dataset has already been processed")
        sys.exit(0)
    
    return checksum

def getDataUrl():
    context_json = json.loads(urlopen("https://www.covid19.admin.ch/api/data/context").read())
    return context_json['sources']['zip']['csv']

def update_dataset_checksum(checksum):
    Path("./dataset.zip.sha256").touch()
    with open("./dataset.zip.sha256","w") as f:
        f.write(checksum)

if __name__ == "__main__":
    # execute only if run as a script
    main()
