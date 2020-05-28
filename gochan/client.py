from typing import List

from urllib.parse import urlencode
from urllib.request import Request, urlopen

from gochan.parser import ThreadParserD, ThreadParserH, BbsmenuParser, BoardParser
from gochan.models import Bbsmenu, Board, Thread, Response


class Client:
    def __init__(self, proxy: str = None, get_pastlog_from_html=False):
        super().__init__()
        self._proxy = proxy
        self._get_pastlog_from_html = get_pastlog_from_html

    def get_bbsmenu(self) -> Bbsmenu:
        url = "https://menu.5ch.net/bbsmenu.html"
        html = _get_content(url)
        parser = BbsmenuParser(html)

        return parser.bbsmenu()

    def get_board(self, server: str, board: str) -> Board:
        url = f"https://{server}.5ch.net/{board}/subject.txt"
        subject = _get_content(url)
        parser = BoardParser(subject, server, board)
        return parser.board()

    def get_thread(self, server: str, board: str, key: str) -> Thread:
        if self._proxy is not None:
            dat = self._get_thread_p(server, board, key)
            parser = ThreadParserD(dat, server, board)

            if not parser.is_pastlog() or not self._get_pastlog_from_html:
                return parser.thread()

        html = self._get_thread_h(server, board, key)
        parser = ThreadParserH(html, server, board, key)
        return parser.thread()

    def _get_thread_h(self, server: str, board: str, key: str) -> str:
        url = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}/"
        return _get_content(url)

    def _get_thread_p(self, server: str, board: str, key: str) -> str:
        url = f"http://{server}.5ch.net:80/{board}/dat/{key}.dat"
        return _get_content(url, self._proxy)

    def get_responses_after(self, server: str, board: str, key: str, after: int) -> List[Response]:
        url = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}/{after + 1}-"
        html = _get_content(url)
        parser = ThreadParserH(html, server, board, key)
        return parser.responses()[1:]

    def post_response(self, server: str, board: str, key: str, name: str, mail: str, msg: str) -> str:
        url = f"https://{server}.5ch.net/test/bbs.cgi"
        ref = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}"
        params = {"bbs": board, "key": key, "time": "1588219909",
                  "FROM": name, "mail": mail, "MESSAGE": msg, "submit": "書き込み"}

        data = urlencode(params, encoding="shift-jis", errors="xmlcharrefreplace").encode()
        hdrs = {"Referer": ref, "User-Agent": "Mozilla/5.0", "Cookie": "yuki=akari"}

        req = Request(url, headers=hdrs)

        res = urlopen(req, data)
        content = res.read().decode("shift-jis")
        res.close()

        return content


def _get_content(url: str, proxy: str = None) -> str:
    hdr = {"User-Agent": "Mozilla/5.0"}

    req = Request(url, headers=hdr)

    if proxy is not None:
        req.set_proxy(proxy, "http")

    response = urlopen(req)
    content = response.read().decode("shift-jis", "ignore")
    response.close()

    return content


client = Client()
