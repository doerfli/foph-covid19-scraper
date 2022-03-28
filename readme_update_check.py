from urllib.request import urlopen
import json
import re
import zipfile
import os.path
import hashlib
import sys
from checksum import calculate_filehash

def main():
    update_checksum = len(sys.argv) > 1 and sys.argv[1] == "--update"
    download_data()
    checksum = verify_checksum_of_readme(update_checksum)
    if update_checksum:
        update_expected_checksum(checksum)

def verify_checksum_of_readme(update_checksum):
    checksum = calculate_filehash("./dataset/README.md")

    expected_checksum = ""
    with open("./dataset.README.md.sha256","r") as f:
        expected_checksum = f.read()
    
    print("checksum of downloaded README.md: %s" % checksum)
    print("expected checksum of README.md: %s" % expected_checksum)
    
    if (update_checksum):
        return checksum
    if (checksum != expected_checksum):
        print("checksum of downloaded README.md does not match expected checksum")
        exit(1)

def update_expected_checksum(checksum):
    with open("./dataset.README.md.sha256","w") as f:
        f.write(checksum)
    
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
    z.extract("README.md", "./dataset/")

def getDataUrl():
    context_json = json.loads(urlopen("https://www.covid19.admin.ch/api/data/context").read())
    return context_json['sources']['zip']['csv']


if __name__ == "__main__":
    # execute only if run as a script
    main()