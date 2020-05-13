import webbrowser
from subprocess import Popen

from gochan.config import BROWSER_PATH


def open_link(url: str):
    if BROWSER_PATH is None:
        webbrowser.open(url)
    else:
        Popen([BROWSER_PATH, url])
