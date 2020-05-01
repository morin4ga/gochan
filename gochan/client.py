import html
import re
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from gochan.data import Bbsmenu, Board, BoardHeader, Category, Response, Thread, ThreadHeader


def get_thread(server: str, board: str, key: str) -> Thread:
    url = f"https://{server}.5ch.net/test/read.cgi/{board}/{key}/"
    hdr = {"User-Agent": "Mozilla/5.0"}

    req = Request(url, headers=hdr)

    response = urlopen(req)

    soup = BeautifulSoup(response, features="lxml")

    reses = soup.findAll("div", class_="post")

    response.close()

    thread = Thread(server, board, key, soup.find("title").text.strip(), [])

    for res in reses:
        meta = res.select(".meta")[0]
        number = meta.select(".number")[0].text.strip()
        name = meta.select(".name")[0].text.strip()
        date = meta.select(".date")[0].text.strip()
        id = meta.select(".uid")[0].text.strip()

        msg = res.select(".message")[0]

        for br in msg.find_all("br"):
            br.replace_with("\n" + br.text)

        # Remove first space for each line which was not removed by the above conversion
        msg = msg.text.replace("\n ", "\n")
        msg = re.sub("^ ", "", msg)

        thread.responses.append(Response(number, name, date, id, msg))

    return thread


def get_board(server: str, board: str) -> Board:
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


def get_bbsmenu() -> Bbsmenu:
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


def post_response(server: str, board: str, key: str, name: str, mail: str, msg: str) -> str:
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
