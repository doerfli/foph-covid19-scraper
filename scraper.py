from urllib.request import urlopen
import re
import zipfile
import os.path
from scraper_vacc import processVaccData

def main():
    download_data()
    processVaccData()

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
    prefix = "https://www.covid19.admin.ch"
    overview_src = urlopen("%s/en/overview" % prefix).read().decode('utf-8')
    prog = re.compile("href=\"(/api/data/(.+)/sources-csv.zip)\"")
    match = prog.search(overview_src)
    # print(match)
    # print(match.group(1))
    return "%s%s" % (prefix, match.group(1))


if __name__ == "__main__":
    # execute only if run as a script
    main()
