from data import Thread, Response, Board, ThreadHeader, Category, Bbsmenu, BoardHeader
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import html
from pathlib import Path


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

    for (i, line) in enumerate(txt.split("\n")):
        m = re.search(r"^(\d{10})\.dat<>(.*)\((\d{1,})\)$", line)
        if m is not None:
            key = m.group(1).strip()
            title = m.group(2).strip()
            count = m.group(3).strip()

            result.threads.append(ThreadHeader(server, board, key, i, title, int(count)))

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
