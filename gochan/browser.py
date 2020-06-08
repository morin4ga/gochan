import urllib
import webbrowser
from subprocess import Popen
from typing import List

from gochan.config import BROWSER_PATH


def open_link(url: str):
    if BROWSER_PATH is None:
        webbrowser.open(url)
    else:
        Popen([BROWSER_PATH, url])


def open_links(urls: List[str]):
    if BROWSER_PATH is None:
        for url in urls:
            webbrowser.open(url)
    else:
        Popen([BROWSER_PATH, *urls])
