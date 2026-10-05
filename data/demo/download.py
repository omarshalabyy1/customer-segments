"""Demo only: download the demo transactions file into data/input/ (about 45 MB). A client's file is copied there instead."""

import urllib.request
import zipfile
from pathlib import Path

URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
INPUT = Path(__file__).parents[1] / "input"

zip_path = INPUT / "online_retail_ii.zip"
urllib.request.urlretrieve(URL, zip_path)
zipfile.ZipFile(zip_path).extractall(INPUT)
print(f"downloaded to {INPUT}: {', '.join(p.name for p in INPUT.glob('*.xlsx'))}")
