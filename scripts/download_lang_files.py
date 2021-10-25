import collections
import os
import pathlib

from bs4 import BeautifulSoup
import requests


BASE_URL = "http://l10n-files.qt.io/l10n-files/"

r = requests.get(BASE_URL)
data = r.text
soup = BeautifulSoup(data, features="lxml")
TARGET_DIR = pathlib.Path(__file__).parent.parent / "prettyqt" / "localization"

langs = collections.defaultdict(list)
for link in soup.find_all("a"):
    url = link.get("href")
    if url.startswith("qt-old515") and "untranslated" not in url:
        # merging seems to create an invalid qm file, so just qtbase for now
        if "qtbase" not in url:
            continue
        response = requests.get(f"{BASE_URL}/{url}")
        response.encoding = "utf-8"
        filename = url.rsplit("/", 1)[1].replace("qt_help", "qthelp")
        file = TARGET_DIR / filename
        with file.open("w", encoding="utf-8") as f:
            f.write(response.text)
        split = str(file).split("_", maxsplit=1)
        lang = split[1][:-3]
        langs[lang].append(str(file))

for k, v in langs.items():
    target = TARGET_DIR / f"language_{k}.qm"
    cmd = f"lrelease -compress {' '.join(v)} -qm {target}"
    os.system(cmd)
    for path in v:
        pathlib.Path(path).unlink()
