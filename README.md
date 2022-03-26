# foph-covid19-scraper

Scraper for covid 19 vaccination data provided by FOPH via https://www.covid19.admin.ch/en/overview

## Execute scaper

```
python scraper.py
```

## Execute README.md update checker

```
python readme_update_check.py
```

Will return with exit code 1 if checksum in `dataset.README.md.sha256` does not match.

### Update expected checksum

```
python readme_update_check.py --update
```

Will update checksum in `dataset.README.md.sha256`.