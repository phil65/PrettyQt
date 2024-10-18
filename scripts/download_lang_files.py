# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "bs4",
#   "requests",
#   "lxml",
#   "tqdm",
# ]
# ///

import collections
import pathlib
import subprocess

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm


BASE_URL = "http://l10n-files.qt.io/l10n-files/"
TARGET_DIR = pathlib.Path(__file__).parent.parent / "prettyqt" / "localization"
LRELEASE_CMD = "pyside6-lrelease"
LANGUAGE_VERSION = "qt-current"


def fetch_html_content(url: str) -> str:
    """Fetch HTML content from the given URL.

    Args:
        url: The URL to fetch the HTML content from.

    Returns:
        str: The HTML content as a string.

    Raises:
        requests.HTTPError: If the HTTP request fails.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_links(html_content: str) -> list[str]:
    """Parse HTML content and extract relevant links.

    Args:
        html_content: The HTML content to parse.

    Returns:
        List[str]: A list of relevant URLs extracted from the HTML content.
    """
    soup = BeautifulSoup(html_content, features="lxml")
    return [
        link.get("href")
        for link in soup.find_all("a")
        if isinstance(link.get("href"), str)
        and link.get("href").startswith(LANGUAGE_VERSION)
        and "untranslated" not in link.get("href")
        and "qtbase" in link.get("href")
    ]


def download_and_save_file(url: str, target_dir: pathlib.Path) -> pathlib.Path:
    """Download a file from the given URL and save it to the target directory.

    Args:
        url: The URL of the file to download.
        target_dir: The directory to save the downloaded file.

    Returns:
        pathlib.Path: The path of the saved file.

    Raises:
        requests.HTTPError: If the HTTP request fails.
    """
    response = requests.get(url)
    response.raise_for_status()
    response.encoding = "utf-8"
    filename = url.rsplit("/", 1)[1].replace("qt_help", "qthelp")
    file_path = target_dir / filename
    file_path.write_text(response.text, encoding="utf-8")
    return file_path


def process_language_files(
    links: list[str], target_dir: pathlib.Path
) -> dict[str, list[str]]:
    """Process language files and return a dictionary of language codes and file paths.

    Args:
        links: A list of URLs to process.
        target_dir: The directory to save the downloaded files.

    Returns:
        Dict[str, List[str]]: A dictionary mapping language codes to lists of file paths.
    """
    langs: dict[str, list[str]] = collections.defaultdict(list)
    with tqdm(total=len(links), desc="Downloading language files") as pbar:
        for link in links:
            pbar.set_description(f"Downloading {link}")
            file_path = download_and_save_file(f"{BASE_URL}/{link}", target_dir)
            lang_code = str(file_path).split("_", maxsplit=1)[1][:-3]
            langs[lang_code].append(str(file_path))
            pbar.update(1)
    return langs


def compile_language_files(langs: dict[str, list[str]], target_dir: pathlib.Path):
    """Compile language files using lrelease and clean up temporary files.

    Args:
        langs: A dictionary mapping language codes to lists of file paths.
        target_dir: The directory to save the compiled language files.

    Raises:
        subprocess.CalledProcessError: If the lrelease command fails.
    """
    with tqdm(total=len(langs), desc="Compiling language files") as pbar:
        for lang_code, file_paths in langs.items():
            target = target_dir / f"language_{lang_code}.qm"
            pbar.set_description(f"Compiling {target}")
            cmd = [LRELEASE_CMD, "-compress", *file_paths, "-qm", str(target)]
            subprocess.run(cmd, check=True, text=True, capture_output=True)
            for path in file_paths:
                pathlib.Path(path).unlink()
            pbar.update(1)


def main():
    """Main function to orchestrate the language file download and processing.

    This function performs the following steps:
    1. Create the target directory if it doesn't exist.
    2. Fetch the HTML content from the base URL.
    3. Parse the HTML content to extract relevant links.
    4. Process the language files by downloading and saving them.
    5. Compile the language files and clean up temporary files.

    Raises:
        requests.HTTPError: If any HTTP request fails.
        subprocess.CalledProcessError: If the lrelease command fails.
    """
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    html_content = fetch_html_content(BASE_URL)
    links = parse_links(html_content)
    langs = process_language_files(links, TARGET_DIR)
    compile_language_files(langs, TARGET_DIR)


if __name__ == "__main__":
    main()
