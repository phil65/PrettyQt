import pathlib

from bs4 import BeautifulSoup
import requests


BASE_URL = "http://l10n-files.qt.io/l10n-files/"

r = requests.get(BASE_URL)
data = r.text
soup = BeautifulSoup(data)
target_dir = pathlib.Path(__file__).parent.parent / "prettyqt" / "localization"

for link in soup.find_all("a"):
    url = link.get("href")
    if url.startswith("qt5-stable") and "untranslated" not in url:
        response = requests.get(f"{BASE_URL}/{url}")
        response.encoding = "utf-8"
        filename = url.rsplit("/", 1)[1].replace("qt_help", "qthelp")
        file = target_dir / filename
        with file.open("w", encoding="utf-8") as f:
            f.write(response.text)
        # print(response.text)
        # break
