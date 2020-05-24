import html
import re
import time
from html import unescape
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from gochan.data import Bbsmenu, Board, BoardHeader, Category, Response, Thread, ThreadHeader


class Client:
    def __init__(self, proxy: str = None, use_proxy=False, get_pastlog_from_html=False):
        super().__init__()
        self._proxy = proxy
        self._use_proxy = use_proxy
        self._get_pastlog_from_html = get_pastlog_from_html

    def get_bbsmenu(self) -> Bbsmenu:
        url = "https://menu.5ch.net/bbsmenu.html"
        hdr = {"User-Agent": "Mozilla/5.0"}

        req = Request(url, headers=hdr)

        response = urlopen(req)
        content = response.read().decode("shift-jis")
        response.close()

        cat_elems = content.split("<br><br>")

        catname_reg = re.compile(r"<B>(.*?)</B><br>")
        board_reg = re.compile(r"<A HREF=http://(.*?).5ch.net/(.*?)/>(.*?)</A>")

        bbsmenu = Bbsmenu([])

        for cat_elem in cat_elems:
            lines = cat_elem.split("\n")

            if len(lines) == 0:
                continue

            m1 = catname_reg.search(lines.pop(0))

            if m1 is None:
                continue

            category_name = m1.group(1).strip()

            if category_name == "他のサイト":
                continue

            category = Category(category_name, [])

            for line in lines:
                m2 = board_reg.search(line)

                if m2 is None:
                    continue

                server = m2.group(1).strip()
                board = m2.group(2).strip()
                name = m2.group(3).strip()

                category.boards.append(BoardHeader(server, board, name))

            bbsmenu.categories.append(category)

        return bbsmenu

    def get_board(self, server: str, board: str) -> Board:
        url = f"https://{server}.5ch.net/{board}/subject.txt"
        hdr = {"User-Agent": "Mozilla/5.0"}

        req = Request(url, headers=hdr)

        response = urlopen(req)
        content = response.read().decode("shift-jis", "ignore")
        response.close()

        txt = html.unescape(content)

        result = Board(server, board, [])

        now = int(time.time())
        for (i, line) in enumerate(txt.split("\n"), 1):
            m = re.search(r"^(\d{10})\.dat<>(.*)\((\d{1,})\)$", line)
            if m is not None:
                key = m.group(1).strip()
                title = m.group(2).strip()
                count = int(m.group(3).strip())

                since = int(key)

                diff = now - since

                speed = 0

                if diff > 0:
                    res_per_s = count / diff
                    speed = int(res_per_s * 60 * 60 * 24)

                result.threads.append(ThreadHeader(server, board, key, i, title, count, speed))

        return result

    def get_thread(self, server: str, board: str, key: str) -> Thread:
        if self._use_proxy:
            t = self._get_thread_p()

            if t.is_pastlog and self._get_pastlog_from_html:
                t = self._get_thread_h(server, board, key)

            return t
        else:
            return self._get_thread_h(server, board, key)

    def _get_thread_h(self, server: str, board: str, key: str) -> Thread:
        url = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}/"
        hdr = {"User-Agent": "Mozilla/5.0"}

        req = Request(url, headers=hdr)

        response = urlopen(req)

        html = response.read().decode("shift-jis", "ignore")

        response.close()

        t = _parse_html(html)
        t.server = server
        t.board = board
        t.key = key

        return t

    def _get_thread_p(self, server: str, board: str, key: str) -> Thread:
        url = f"http://{server}.5ch.net:80/{board}/dat/{key}.dat"
        hdr = {"User-Agent": "Mozilla/5.0"}

        req = Request(url, headers=hdr)
        req.set_proxy(self._proxy, "http")

        response = urlopen(req)
        dat = response.read().decode("shift-jis")
        response.close()

        t = _parse_dat(dat)
        t.server = server
        t.board = board
        t.key = key

        return t

    def update_thread(self, thread: Thread):
        url = f"https://{thread.server}.5ch.net/test/read.cgi/{thread.board}/{thread.key}/{len(thread.responses)+1}-"
        hdr = {"User-Agent": "Mozilla/5.0"}

        req = Request(url, headers=hdr)

        response = urlopen(req)

        html = response.read().decode("shift-jis", "ignore")

        response.close()

        t = _parse_html(html)
        thread.responses.extend(t.responses[1:])
        thread.is_pastlog = t.is_pastlog

    def post_response(self, server: str, board: str, key: str, name: str, mail: str, msg: str) -> str:
        url = f"https://{server}.5ch.net/test/bbs.cgi"
        ref = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}"
        params = {"bbs": board, "key": key, "time": "1588219909",
                  "FROM": name, "mail": mail, "MESSAGE": msg, "submit": "書き込み"}

        data = urlencode(params, encoding="shift-jis").encode()
        hdrs = {"Referer": ref, "User-Agent": "Mozilla/5.0", "Cookie": "yuki=akari"}

        req = Request(url, headers=hdrs)

        res = urlopen(req, data)
        content = res.read().decode("shift-jis")
        res.close()

        return content


def _parse_dat(dat: str) -> Thread:
    lines = dat.split("\n")

    title = re.search(r".*<>(.*?)$", lines[0]).group(1)
    thread = Thread(None, None, None, title, [], False)
    total_links = 0

    re_res = re.compile(r"(.*?)<>(.*?)<>(.*? .*?) (.*?)<> (.*?) <>.*")
    re_b = re.compile(r"</?b>")
    re_img = re.compile(r'<a class="image".*?>(.*?)</a>')
    re_link = re.compile(r'(http.*?)(?: |$)')

    for i, l in enumerate(lines, 1):
        m = re_res.search(l)

        if m is None:
            continue

        name = re_b.sub("", m.group(1))
        mail = m.group(2)
        date = m.group(3)
        id = m.group(4)
        msg = m.group(5)

        msg = re.sub(" ?<br> ", "\n", msg)

        for img in re_img.finditer(msg):
            thread.links.append(img.group(1))
            msg, _ = re_img.subn(r"\1(" + str(total_links) + ")", msg)
            total_links += 1

        for link in re_link.finditer(msg):
            thread.links.append(link.group(1))
            msg, _ = re_link.subn(r"\1(" + str(total_links) + ")")
            total_links += 1

        r = Response(i, name, mail, date, id, msg)
        thread.responses.append(r)

    if len(thread.responses) == 2 and thread.responses[1].name == "５ちゃんねる ★"\
            and thread.responses[1].message.startswith("このスレッドは過去ログです"):
        thread.is_pastlog = True

    return thread


def _parse_html(html: str) -> Thread:
    title = re.search("<title>(.*?)\n</title>", html).group(1)

    is_pastlog = re.search('<div class="stoplight stopred stopdone', html) is None

    thread = Thread(None, None, None, title, [], is_pastlog)

    total_links = 0

    re_res = re.compile(
        r'<div class="post" id="(\d+)".*?"name"><b>(?:<a href="mailto:(.*?)">)?(.*?)(?:</a>)?</b></span>.*?"date">(.*?)'
        r'<.*?"uid">(.*?)<.*?>(?:<.*?>)+? (.*?) (?:<.*?>)+?</div></div><br>'
    )

    re_link = re.compile(r'<a href="http.*?>(.*?)</a>|<a class="image".*?>(.*?)</a>')

    re_anchor = re.compile(r'<a href.*?class="reply_link">(.*?)</a>')

    re_b = re.compile(r'</?b>')

    for res in re_res.finditer(html):
        number = res.group(1)
        mail = res.group(2)
        name = re_b.sub("", res.group(3))
        date = res.group(4)
        id = res.group(5)
        msg = res.group(6)
        msg = re.sub(" ?<br> ", "\n", msg)
        # Remove be icon
        msg = re.sub(r'<img.*\n', "", msg)

        for link in re_link.finditer(msg):
            if link.group(1) is not None:
                thread.links.append(link.group(1))
                msg, _ = re_link.subn(r"\1(" + str(total_links) + ")", msg, 1)
            else:
                thread.links.append(link.group(2))
                msg, _ = re_link.subn(r"\2(" + str(total_links) + ")", msg, 1)

            total_links += 1

        for anchor in re_anchor.finditer(msg):
            msg, _ = re_anchor.subn(r"\1", msg, 1)

        msg = unescape(msg)

        thread.responses.append(
            Response(number, name, mail, date, id, msg)
        )

    return thread


client = Client()
